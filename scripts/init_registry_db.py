#!/usr/bin/env python3
"""Create (or migrate) the SQLite registry database the server uses.

The schema is owned by ``core.storage`` (a single source of truth shared with
the runtime), so this script just points :func:`core.storage.init` at a target
path and reports where the database lives. It is idempotent: running it again on
an existing database is a no-op (``CREATE TABLE/INDEX IF NOT EXISTS`` plus the
lossless legacy migration in ``core.storage``).

Usage::

    python scripts/init_registry_db.py [DB_PATH]

``DB_PATH`` is optional. When omitted the target is resolved exactly like the
server does at runtime:

- ``$MCP_STATE_DIR/registry.db`` if that environment variable is set (the
  container/deployment convention, e.g. ``C:\\state``), otherwise
- the platform user-data location (``platformdirs.user_data_dir``).

Typical use is to pre-create ``registry.db`` on a freshly mounted volume before
starting the server:

    MCP_STATE_DIR=C:\\state python scripts/init_registry_db.py

Exit code is 0 on success (including "already exists") and non-zero if the
database cannot be created or verified.
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

# Make ``core`` importable when this script runs from a source checkout
# (sys.path[0] is ``scripts/`` when invoked as ``python scripts/init_registry_db.py``).
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core import storage  # noqa: E402  (import after sys.path setup)


def _describe_schema(db_path: Path) -> str:
    """Human-readable list of the tables/views/indexes present in the database."""
    with sqlite3.connect(str(db_path)) as conn:
        tables = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name"
            )
        ]
        indexes = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'index' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
    return f"tables: {', '.join(tables) or '(none)'}; indexes: {', '.join(indexes) or '(none)'}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "db_path",
        nargs="?",
        default=None,
        help="Explicit registry.db path (default: $MCP_STATE_DIR/registry.db, "
        "else the platform user-data directory).",
    )
    args = parser.parse_args(argv)

    try:
        # Passing None resolves the same default the server uses at runtime; an
        # explicit argument wins. init() creates the parent directory, applies
        # the schema and the legacy migration, then returns the resolved path.
        db_path = storage.init(db_path=Path(args.db_path) if args.db_path else None)
    except Exception as exc:  # pragma: no cover - defensive; init errors are rare
        print(f"error: could not create the registry database: {exc}", file=sys.stderr)
        return 1

    print(f"registry database ready: {db_path}")
    print(f"schema: {_describe_schema(db_path)}")

    env_state_dir = os.getenv("MCP_STATE_DIR")
    if env_state_dir and Path(env_state_dir).resolve() != db_path.resolve().parent:
        print(
            f"note: MCP_STATE_DIR is set to {env_state_dir!r}, but the database was "
            f"created under {db_path.parent!r} (explicit path wins).",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
