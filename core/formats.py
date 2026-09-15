"""Format metadata and save-options mapping for Aspose.Cells Cloud.

These lists are the single source of truth for what the MCP server advertises:

- :func:`list_supported_load_formats` advertises only spreadsheet/data source
  formats that Aspose.Cells can actually open (no e-book formats, no OCR).
- :func:`list_supported_save_formats` is *derived* from the same table used by
  :func:`get_save_options_with_save_format`, so every advertised save target can
  demonstrably be routed through typed save options and the two can never drift
  apart (see tests/test_core_formats.py).

Descriptions are factual one-liners aimed at an LLM caller; they do not invent
local parsing/OCR capabilities (all processing happens in the Aspose Cloud API).
"""

from asposecellscloud import (
    DbfSaveOptions,
    DifSaveOptions,
    DocxSaveOptions,
    HtmlSaveOptions,
    ImageSaveOptions,
    JsonSaveOptions,
    MarkdownSaveOptions,
    OdsSaveOptions,
    OoxmlSaveOptions,
    PdfSaveOptions,
    PclSaveOptions,
    PptxSaveOptions,
    SqlScriptSaveOptions,
    TxtSaveOptions,
    XlsSaveOptions,
    XlsbSaveOptions,
    XmlSaveOptions,
    XpsSaveOptions,
)

# Canonical key (lowercase) -> (extension, one-line factual description, builder).
# The builder receives the caller's original-case format string because a few
# SDK options constructors take the target format as an argument; this preserves
# the exact behaviour of the pre-registry implementation.
_SAVE_FORMATS = {
    "csv": (".csv", "Comma-separated values.", lambda fmt: TxtSaveOptions()),
    "tsv": (".tsv", "Tab-separated values.", lambda fmt: TxtSaveOptions()),
    "xls": (".xls", "Legacy Excel 97-2003 workbook.", lambda fmt: XlsSaveOptions()),
    "xlsx": (".xlsx", "Modern Excel workbook (Office Open XML).", lambda fmt: OoxmlSaveOptions(save_format=fmt)),
    "xlsb": (".xlsb", "Excel binary workbook.", lambda fmt: XlsbSaveOptions(save_format=fmt)),
    "xlsm": (".xlsm", "Excel macro-enabled workbook.", lambda fmt: OoxmlSaveOptions(save_format=fmt)),
    "xltx": (".xltx", "Excel template.", lambda fmt: OoxmlSaveOptions(save_format=fmt)),
    "html": (".html", "HTML web page.", lambda fmt: HtmlSaveOptions(save_format=fmt)),
    "mhtml": (".mhtml", "Single-file MHTML web archive.", lambda fmt: HtmlSaveOptions(save_format=fmt)),
    "ods": (".ods", "OpenDocument spreadsheet (LibreOffice / OpenOffice).", lambda fmt: OdsSaveOptions(save_format=fmt)),
    "ots": (".ots", "OpenDocument spreadsheet template.", lambda fmt: OdsSaveOptions(save_format=fmt)),
    "fods": (".fods", "OpenDocument flat XML spreadsheet.", lambda fmt: OdsSaveOptions(save_format=fmt)),
    "xml": (".xml", "SpreadsheetML XML.", lambda fmt: XmlSaveOptions()),
    "json": (".json", "JSON data export.", lambda fmt: JsonSaveOptions()),
    "markdown": (".md", "Markdown document.", lambda fmt: MarkdownSaveOptions()),
    "dif": (".dif", "Data Interchange Format.", lambda fmt: DifSaveOptions(save_format=fmt)),
    "dbf": (".dbf", "dBASE database file.", lambda fmt: DbfSaveOptions()),
    "docx": (".docx", "Microsoft Word document.", lambda fmt: DocxSaveOptions()),
    "pptx": (".pptx", "Microsoft PowerPoint presentation.", lambda fmt: PptxSaveOptions()),
    "xps": (".xps", "XML Paper Specification.", lambda fmt: XpsSaveOptions()),
    "pdf": (".pdf", "Portable Document Format.", lambda fmt: PdfSaveOptions()),
    "pcl": (".pcl", "Printer Command Language.", lambda fmt: PclSaveOptions()),
    "sql": (".sql", "SQL insert script.", lambda fmt: SqlScriptSaveOptions()),
    "tiff": (".tiff", "TIFF image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
    "svg": (".svg", "SVG image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
    "emf": (".emf", "Windows Enhanced Metafile image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
    "jpg": (".jpg", "JPEG image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
    "png": (".png", "PNG image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
    "bmp": (".bmp", "Windows Bitmap image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
    "gif": (".gif", "GIF image.", lambda fmt: ImageSaveOptions(image_format=fmt)),
}

_LOAD_FORMATS = [
    {"format": "CSV", "ext": ".csv", "desc": "Comma-separated values."},
    {"format": "XLS", "ext": ".xls", "desc": "Legacy Excel 97-2003 workbook."},
    {"format": "XLSX", "ext": ".xlsx", "desc": "Modern Excel workbook (Office Open XML)."},
    {"format": "TSV", "ext": ".tsv", "desc": "Tab-separated values."},
    {"format": "HTML", "ext": ".html", "desc": "HTML document (tables read as worksheets)."},
    {"format": "MHTML", "ext": ".mhtml", "desc": "Single-file MHTML web archive."},
    {"format": "XHTML", "ext": ".xhtml", "desc": "XHTML document."},
    {"format": "ODS", "ext": ".ods", "desc": "OpenDocument spreadsheet (LibreOffice / OpenOffice)."},
    {"format": "XLSB", "ext": ".xlsb", "desc": "Excel binary workbook."},
    {"format": "DIF", "ext": ".dif", "desc": "Data Interchange Format."},
    {"format": "OTS", "ext": ".ots", "desc": "OpenDocument spreadsheet template."},
    {"format": "XML", "ext": ".xml", "desc": "SpreadsheetML XML."},
    {"format": "NUMBERS", "ext": ".numbers", "desc": "Apple Numbers spreadsheet."},
    {"format": "FODS", "ext": ".fods", "desc": "OpenDocument flat XML spreadsheet."},
    {"format": "SXC", "ext": ".sxc", "desc": "StarOffice / OpenOffice.org 1.x Calc spreadsheet."},
    {"format": "JSON", "ext": ".json", "desc": "JSON structured data."},
    {"format": "DBF", "ext": ".dbf", "desc": "dBASE database file."},
]

def list_supported_load_formats():
    """List source (read/import) formats Aspose.Cells Cloud can open."""
    return [dict(entry) for entry in _LOAD_FORMATS]


def list_supported_save_formats():
    """List target (save/export) formats routable through typed save options.

    Names are returned in canonical uppercase (e.g. ``PDF``) so callers can pass
    them straight back as ``target_format`` / ``format`` arguments.
    """
    return [
        {"format": name.upper(), "ext": ext, "desc": desc}
        for name, (ext, desc, _builder) in _SAVE_FORMATS.items()
    ]


def get_save_options_with_save_format(save_format: str):
    """Return a typed save-options instance for ``save_format``, or ``None``.

    ``save_format`` is matched case-insensitively. When a concrete options model
    exists for the format it is returned as an *instance* (never a class); the
    caller can then set attributes such as fit modes or JSON-provided options.
    """
    key = (save_format or "").strip().lower()
    entry = _SAVE_FORMATS.get(key)
    if entry is None:
        return None
    return entry[2](save_format)


# Scaling modes that map to a real save-options attribute.
_FIT_ATTRS = {
    "fitsheetononepage": "one_page_per_sheet",
    "fitallcolumnsononepage": "all_columns_in_one_page_per_sheet",
    # "FitAllRowsOnOnePage" is intentionally absent: none of the Aspose.Cells
    # Cloud save-options models declare an attribute for it, so requesting it
    # is an explicit error instead of a silent no-op (see apply_fit_mode).
}


def apply_fit_mode(save_options, scaling_mode: str) -> None:
    """Apply a documented print-scaling mode to save options in place.

    The mode is matched case-insensitively. Instead of silently ignoring a mode
    the selected options model cannot honour, a :class:`ValueError` is raised so
    callers/agents get a clear, actionable error:

    - unknown modes are rejected;
    - ``FitAllRowsOnOnePage`` is rejected (no Aspose.Cells save-options model
      supports it);
    - a fit mode that the concrete options model does not declare (e.g.
      ``FitAllColumnsOnOnePage`` on PDF) is rejected for that target format.

    ``None`` options, an empty mode and ``NoScaling`` are no-ops.
    """
    if save_options is None or not (scaling_mode or "").strip():
        return
    mode = scaling_mode.strip().lower()
    if mode == "noscaling":
        return
    if mode == "fitallrowsononepage":
        raise ValueError(
            "scaling_mode 'FitAllRowsOnOnePage' is not supported by Aspose.Cells Cloud "
            "save options; use 'FitSheetOnOnePage' or 'FitAllColumnsOnOnePage' instead."
        )
    attr = _FIT_ATTRS.get(mode)
    if attr is None:
        raise ValueError(
            f"Unknown scaling_mode {scaling_mode!r}. Supported modes: NoScaling, "
            "FitSheetOnOnePage, FitAllColumnsOnOnePage."
        )
    if not hasattr(save_options, attr):
        raise ValueError(
            f"scaling_mode {scaling_mode!r} is not supported by "
            f"{type(save_options).__name__} for the requested target format."
        )
    setattr(save_options, attr, True)
