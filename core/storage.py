"""SQLite-backed file-handle registry for Aspose Cloud Storage files.

A file's **uuid is its unique id** — the value handed to MCP callers and passed
back on later calls. Different users may upload files with the same real name;
the uuid is what guarantees uniqueness, never the file name. The cloud location
is a *pure function* of the uuid and the stored object name:

- one cloud file per uuid, at ``<uuid>/<name>`` (``folder=<uuid>``). The object
  ``name`` is the upload's own file name when one is supplied, else the default
  ``File`` — so an upload of ``report.xlsx`` lives at ``<uuid>/report.xlsx`` and
  an unnamed upload at ``<uuid>/File``. This mirrors the ``folder`` + ``name``
  arguments used by the Aspose Cells Cloud "remote spreadsheet" APIs; because the
  folder is the unique uuid, no two uploads ever collide even when they share a
  name.

The file is created by targeting the *uuid folder itself* with the upload
request (:func:`upload_folder`): the Cells storage upload endpoint treats its
``path`` argument as the destination **folder** and names the object after the
uploaded part, so uploading to the folder with the part named ``<name>`` is what
makes ``<uuid>/<name>`` exist. Every consumer (download, edits, save-as source)
then addresses the file at that ``<folder>/<name>`` — which is why the upload
must *not* be pointed at :func:`path_for` itself (that would store the object one
folder deeper than consumers look for it).

The folder is always the uuid (derivable), so the only location piece the
registry must remember is the object ``name`` (the upload's file name, or the
default ``File``) — together with the other metadata that cannot be derived from
the uuid (original human file name, provenance, timestamps, two-phase conversion
state and an optional TTL). All of it lives in SQLite, so the registry stays tiny
and offers transaction-safe writes, cheap existence checks and GC bookkeeping
without scanning the cloud.

This server is unauthenticated today (directly usable); when Aspose Cloud
authentication is integrated later, per-account scoping can be layered on top
without touching the uuid/layout model.

The database file lives under ``MCP_STATE_DIR`` (or the platform user-data
directory) and should sit on a writable volume in containers.

The registry is internal: no MCP tools are exposed here. Callers use
:func:`create` / :func:`allocate` when producing a file and :func:`resolve` /
:func:`path_for` when consuming one.
"""

import os
import sqlite3
import time
import uuid as _uuid
from pathlib import Path

# Storage layout (see module docstring): folder == uuid; object name is the
# upload's file_name when provided, else this default.
INNER_FILE_NAME = "File"

# Row ``status`` values.
_STATUS_READY = "ready"
_STATUS_ALLOCATED = "allocated"


def _default_db_path() -> Path:
    state_dir = os.getenv("MCP_STATE_DIR")
    if state_dir:
        return Path(state_dir) / "registry.db"
    # platformdirs is a declared dependency; import lazily so importing this
    # module never requires it (hermetic tests always init with a temp path).
    from platformdirs import user_data_dir

    return Path(user_data_dir("aspose-cells-cloud-mcp")) / "registry.db"


_DB_PATH: Path | None = None


def _db_path() -> Path:
    if _DB_PATH is None:
        return _default_db_path()
    return _DB_PATH


_SCHEMA = """
CREATE TABLE IF NOT EXISTS file_handles (
    uuid          TEXT PRIMARY KEY,
    original_name TEXT,
    name          TEXT NOT NULL DEFAULT 'File',  -- cloud object name under folder=uuid
    source        TEXT NOT NULL DEFAULT 'uploaded',
    status        TEXT NOT NULL DEFAULT 'ready',  -- 'allocated' | 'ready'
    created_at    INTEGER NOT NULL,
    last_used_at  INTEGER NOT NULL,
    expires_at    INTEGER
);
"""

_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_file_handles_expires ON file_handles(expires_at);
CREATE INDEX IF NOT EXISTS idx_file_handles_name ON file_handles(original_name);
"""


def init(db_path=None) -> Path:
    """Point the registry at ``db_path`` (default: env/platform dir) and create it.

    Safe to call repeatedly; returns the resolved database path. Databases from
    earlier designs (a ``folder``/``name`` mapping table and/or a ``token``
    primary key) are rebuilt losslessly onto the ``uuid``-keyed metadata schema.
    """
    global _DB_PATH
    path = Path(db_path) if db_path else _default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    _DB_PATH = path
    with sqlite3.connect(path) as conn:
        conn.executescript(_SCHEMA)
        _migrate_legacy(conn)       # pre-uuid (token/folder/name) schema, if present
        _migrate_name_column(conn)  # uuid schema without the object `name` column
        conn.executescript(_INDEXES)
    return path


def _migrate_legacy(conn: sqlite3.Connection) -> None:
    """Rebuild a pre-``uuid`` table into the uuid-keyed, metadata-first schema.

    Old designs stored the primary key in a ``token`` column and duplicated
    ``folder``/``name``. ``token`` maps to ``uuid`` and ``folder`` (always equal)
    is derived, but the real cloud object ``name`` is carried over losslessly so
    existing handles keep pointing at their file.
    """
    columns = [row[1] for row in conn.execute("PRAGMA table_info(file_handles)")]
    if "uuid" in columns:
        return
    has_name = "name" in columns
    select_name = "name" if has_name else repr(INNER_FILE_NAME)
    conn.executescript(
        f"""
        ALTER TABLE file_handles RENAME TO file_handles_legacy;
        CREATE TABLE file_handles (
            uuid          TEXT PRIMARY KEY,
            original_name TEXT,
            name          TEXT NOT NULL DEFAULT 'File',
            source        TEXT NOT NULL DEFAULT 'uploaded',
            status        TEXT NOT NULL DEFAULT 'ready',
            created_at    INTEGER NOT NULL,
            last_used_at  INTEGER NOT NULL,
            expires_at    INTEGER
        );
        INSERT INTO file_handles
            (uuid, original_name, name, source, status, created_at, last_used_at, expires_at)
        SELECT token, original_name, {select_name}, source, status,
               created_at, last_used_at, expires_at
            FROM file_handles_legacy;
        DROP TABLE file_handles_legacy;
        """
    )


def _migrate_name_column(conn: sqlite3.Connection) -> None:
    """Add the cloud object ``name`` column to a uuid-keyed schema that lacks it.

    Older ``uuid``-schema databases stored only ``original_name`` (metadata) and
    derived the object name as the constant ``File``. Such rows' real cloud
    objects are named ``File``, so backfill with that default.
    """
    columns = [row[1] for row in conn.execute("PRAGMA table_info(file_handles)")]
    if "name" in columns:
        return
    conn.execute(
        f"ALTER TABLE file_handles ADD COLUMN name TEXT NOT NULL DEFAULT '{INNER_FILE_NAME}'"
    )


def _connect() -> sqlite3.Connection:
    if _DB_PATH is None:
        init()  # lazy first-use: create the default DB so callers need no setup
    conn = sqlite3.connect(str(_db_path()), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _now() -> int:
    return int(time.time())


def _default_ttl_seconds(ttl_seconds: int | None) -> int | None:
    """Effective TTL: explicit argument wins, otherwise ``MCP_FILE_TTL_HOURS`` env."""
    if ttl_seconds is not None:
        return ttl_seconds
    raw = os.getenv("MCP_FILE_TTL_HOURS")
    if raw:
        try:
            return int(float(raw) * 3600)
        except ValueError:
            return None
    return None


def _expires_at(ttl_seconds: int | None, now: int) -> int | None:
    ttl = _default_ttl_seconds(ttl_seconds)
    return now + ttl if ttl else None


def _handle(row) -> dict:
    """Row dict plus the derived cloud-location fields every caller relies on."""
    handle = dict(row)
    handle["folder"] = handle["uuid"]          # derived, never stored
    handle["name"] = row["name"] or INNER_FILE_NAME  # stored cloud object name
    return handle


def object_name(file_name: str | None) -> str:
    """Cloud object name to store a file under, derived from a human file name.

    Reduces ``file_name`` to a single, safe storage-path segment and falls back
    to the default (``File``) when it is absent, empty or unusable — matching
    the ``name`` a resolved handle reports, so the upload key and every later
    lookup always agree. Converted outputs pass ``None`` and get the default.
    """
    if not file_name or not file_name.strip():
        return INNER_FILE_NAME
    cleaned = file_name.strip()
    # keep only the final path segment on both separator conventions
    for sep in ("/", "\\"):
        cleaned = cleaned.rpartition(sep)[2]
    cleaned = cleaned.strip()
    if not cleaned or cleaned in (".", ".."):
        return INNER_FILE_NAME
    return cleaned


# Best-effort GC throttle: expired handles are purged opportunistically on file
# insertion (the main source of registry growth) so long-lived servers do not
# accumulate dead rows. Deleting the orphaned *cloud* files is a separate
# best-effort concern; this only keeps the registry bounded.
_GC_INTERVAL_SECONDS = 60.0
_last_gc_monotonic = 0.0


def _maybe_purge_expired() -> None:
    """Purge expired handles at most once per ``_GC_INTERVAL_SECONDS`` (best effort)."""
    global _last_gc_monotonic
    now_mono = time.monotonic()
    if now_mono - _last_gc_monotonic < _GC_INTERVAL_SECONDS:
        return
    _last_gc_monotonic = now_mono
    try:
        purge_expired()
    except Exception:
        pass  # GC is best-effort; never fail a file registration because of it


def _insert(uuid: str, original_name, name: str, source: str, status: str,
            ttl_seconds: int | None, now: int) -> None:
    _maybe_purge_expired()
    expires = _expires_at(ttl_seconds, now)
    with _connect() as conn:
        conn.execute(
            "INSERT INTO file_handles "
            "(uuid, original_name, name, source, status, created_at, last_used_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (uuid, original_name, name, source, status, now, now, expires),
        )


def create(original_name: str | None = None, source: str = "uploaded",
           ttl_seconds: int | None = None, uuid: str | None = None,
           name: str | None = None) -> str:
    """Register a new upload and return its file uuid.

    ``name`` is the cloud object name the file is (or will be) stored under in
    the ``<uuid>`` folder; it defaults to :func:`object_name` of
    ``original_name`` — i.e. an upload named ``report.xlsx`` is stored at
    ``<uuid>/report.xlsx``, an unnamed one at ``<uuid>/File``. The row is created
    ``ready``; the caller then writes the bytes to :func:`upload_folder`'s
    location. ``uuid`` is only overridable for tests.
    """
    name = name or object_name(original_name)
    uuid = uuid or _uuid.uuid4().hex
    _insert(uuid, original_name, name, source, _STATUS_READY, ttl_seconds, _now())
    return uuid


def allocate(original_name: str | None = None, source: str = "converted", name: str | None = None, ttl_seconds: int | None = None) -> str:
    """Reserve a file uuid for an output file that does not exist in cloud yet.

    ``name`` is the cloud object name the output will be stored under; when it is
    omitted it falls back to :func:`object_name` of ``original_name`` — i.e. the
    default ``File``, matching :func:`create`. Callers that know the output's
    human name (save-as derives ``book1.pdf`` from its source) pass it so the
    downloaded artifact keeps a meaningful name. The row is created with
    ``status='allocated'`` so :func:`resolve` refuses it until the cloud write
    succeeds; call :func:`commit` on success or :func:`abort` to discard the
    reservation.
    """
    uuid = _uuid.uuid4().hex
    # `name` is NOT NULL in the schema, so it must never be inserted as NULL:
    # object_name() supplies the default for callers that pass neither.
    _insert(uuid, original_name, name or object_name(original_name), source,
            _STATUS_ALLOCATED, ttl_seconds, _now())
    return uuid


def commit(uuid: str) -> None:
    """Mark an allocated file uuid as usable (cloud write succeeded)."""
    with _connect() as conn:
        cur = conn.execute(
            "UPDATE file_handles SET status = ? WHERE uuid = ?",
            (_STATUS_READY, uuid),
        )
    if cur.rowcount == 0:
        raise ValueError(f"Unknown file uuid: {uuid}")


def abort(uuid: str) -> None:
    """Discard a file-uuid reservation (cloud write failed / not performed)."""
    with _connect() as conn:
        conn.execute("DELETE FROM file_handles WHERE uuid = ?", (uuid,))


def _touch(conn: sqlite3.Connection, uuid: str, now: int) -> None:
    conn.execute(
        "UPDATE file_handles SET last_used_at = ? WHERE uuid = ?", (now, uuid)
    )


def resolve(uuid: str) -> dict:
    """Return the handle dict for a usable file uuid, else raise ``ValueError``.

    Raises with a clear message when the uuid is unknown, not yet committed
    (``allocated``) or expired, and refreshes ``last_used_at`` on success. The
    returned dict carries the derived ``folder``/``name`` cloud-location fields.
    """
    now = _now()
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM file_handles WHERE uuid = ?", (uuid,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Unknown or expired file uuid: {uuid}")
        if row["status"] != _STATUS_READY:
            raise ValueError(f"File uuid {uuid} is not ready yet.")
        if row["expires_at"] is not None and row["expires_at"] <= now:
            raise ValueError(f"Unknown or expired file uuid: {uuid}")
        _touch(conn, uuid, now)
        # Re-read so the returned handle reflects the refreshed last_used_at.
        row = conn.execute(
            "SELECT * FROM file_handles WHERE uuid = ?", (uuid,)
        ).fetchone()
        return _handle(row)


def upload_folder(uuid: str) -> str:
    """Destination to give the Cells **upload** request for a file uuid.

    The upload endpoint takes a destination *folder* and creates the object at
    ``<folder>/<part name>`` (see the module docstring), so this is just the
    uuid. Use this for :class:`asposecellscloud.UploadFileRequest`, sending the
    bytes as a part named after the file's :func:`object_name`; consumers then
    address the uploaded file with :func:`path_for` using the handle's ``name``.
    Passing :func:`path_for` here instead would store the object one level too
    deep.
    """
    return uuid


def path_for(uuid: str, name: str | None = None) -> str:
    """Storage path (``<folder>/<name>``) for a file uuid.

    ``name`` defaults to the constant ``File``; callers resolving a real handle
    should pass the handle's ``name`` so named uploads (``<uuid>/report.xlsx``)
    are addressed correctly. The path is a pure function of the uuid + name, so
    no database read is needed; :func:`resolve` is the place to validate that a
    uuid actually exists.
    """
    return f"{uuid}/{name or INNER_FILE_NAME}"


def remove(uuid: str) -> dict | None:
    """Delete the handle row and return it (so the caller can also delete the
    cloud file). Returns ``None`` when the uuid was unknown."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM file_handles WHERE uuid = ?", (uuid,)
        ).fetchone()
        conn.execute("DELETE FROM file_handles WHERE uuid = ?", (uuid,))
    return _handle(row) if row is not None else None


def purge_expired(now: int | None = None) -> list[dict]:
    """Delete expired handles and return them (for best-effort cloud cleanup)."""
    now = now or _now()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM file_handles WHERE expires_at IS NOT NULL AND expires_at <= ?",
            (now,),
        ).fetchall()
        if rows:
            conn.execute(
                "DELETE FROM file_handles WHERE expires_at IS NOT NULL AND expires_at <= ?",
                (now,),
            )
        return [_handle(r) for r in rows]


def count() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM file_handles").fetchone()[0]


def list_files() -> list[dict]:
    """All ready handles (used by future admin/list tools and diagnostics)."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM file_handles WHERE status = ? ORDER BY created_at DESC",
            (_STATUS_READY,),
        ).fetchall()
        return [_handle(r) for r in rows]
