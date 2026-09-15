import os
import socket

from asposecellscloud import CellsApi

# Bounds every HTTP call the Aspose SDK makes. The SDK configures no timeout on
# its urllib3 pool, so without this a stalled backend (or a blackholed route)
# hangs the MCP tool call forever. urllib3 leaves the socket default untouched
# when no explicit timeout is given, so setting it here caps connect+read on all
# SDK requests — including the OAuth token refresh that CellsApi performs in its
# constructor.
_CLOUD_TIMEOUT_ENV = "MCP_CLOUD_TIMEOUT_SECONDS"
_DEFAULT_CLOUD_TIMEOUT = 300.0


def _cloud_timeout() -> float | None:
    """Read the cloud HTTP timeout bound (seconds) for the SDK client.

    ``MCP_CLOUD_TIMEOUT_SECONDS`` overrides the default 300 s. A value ``<= 0``
    (or one that cannot be parsed) disables the bound, restoring the SDK's
    unlimited behaviour.
    """
    raw = os.getenv(_CLOUD_TIMEOUT_ENV)
    if raw is None or str(raw).strip() == "":
        return _DEFAULT_CLOUD_TIMEOUT
    try:
        value = float(raw)
    except ValueError:
        return _DEFAULT_CLOUD_TIMEOUT
    return value if value > 0 else None


def get_cells_cloud_client() -> CellsApi:
    timeout = _cloud_timeout()
    if timeout:
        socket.setdefaulttimeout(timeout)
    client_id = os.getenv("ASPOSE_CLOUD_CLIENT_ID")
    client_secret = os.getenv("ASPOSE_CLOUD_CLIENT_SECRET")
    base_url = os.getenv("ASPOSE_CLOUD_API_URL")
    if base_url is None or len(base_url.strip()) == 0:
        return CellsApi(client_id, client_secret)
    return CellsApi(client_id, client_secret, base_uri=base_url)


def num_to_cell(row: int, col: int) -> str:
    """Convert 0-based (row, col) to A1 notation, e.g. (0, 0) -> 'A1', (0, 25) -> 'Z1'."""
    col += 1
    column_name = ""
    while col > 0:
        col -= 1
        column_name = chr(col % 26 + 65) + column_name
        col //= 26
    return f"{column_name}{row + 1}"


def resolve_worksheet_range(structure, worksheet: str | None, _range: str | None) -> tuple[str, str]:
    """Resolve the target (worksheet_name, cell_range) for a text operation.

    Documented semantics shared by every editing tool:
    - ``worksheet`` ``None``/empty -> the first worksheet of the workbook.
    - ``worksheet`` set -> must match a worksheet name exactly; a ``ValueError``
      is raised otherwise so callers get a clear error instead of a silent no-op.
    - ``_range`` provided -> used verbatim.
    - ``_range`` ``None``/empty -> the used range ``A1:<last data cell>`` of the
      resolved worksheet (falls back to ``A1`` for an empty sheet).

    :param structure: parsed workbook-structure JSON (dict with a ``Worksheets`` list).
    :return: ``(worksheet_name, range_string)``.
    """
    worksheets = (structure or {}).get("Worksheets") or []
    if not worksheets:
        raise ValueError("The workbook contains no worksheets to edit.")

    if worksheet:
        matches = [w for w in worksheets if w.get("Name") == worksheet]
        if not matches:
            raise ValueError(f"Worksheet '{worksheet}' was not found in the workbook.")
        target = matches[0]
    else:
        target = worksheets[0]

    sheet_name = target.get("Name")
    if _range:
        return sheet_name, _range

    max_row = target.get("MaxDataRow", -1)
    max_col = target.get("MaxDataColumn", -1)
    if max_row is None or max_col is None or max_row < 0 or max_col < 0:
        return sheet_name, "A1"
    return sheet_name, f"A1:{num_to_cell(max_row, max_col)}"
