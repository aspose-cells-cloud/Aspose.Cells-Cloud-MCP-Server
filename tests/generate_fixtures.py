"""Generate the sample-workbook fixtures used by the integration tests.

Stdlib only (zipfile + xml escaping) so it runs on any machine without network
or third-party libraries. The generated files are intentionally minimal but
valid, and match the sheet/cell expectations of the MCP integration tests
(e.g. a "Text" worksheet with data in D4 for the text-editing tools).

Usage:
    python tests/generate_fixtures.py
"""

from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

OUT_DIR = Path(__file__).resolve().parent / "fixtures"


def _xlsx(sheets):
    """Build a minimal .xlsx in memory.

    :param sheets: list of (sheet_name, list_of_rows) where each row is a list
                   of (cell_ref, value) and a value that is a str is written as
                   an inline string while everything else is written as a number.
    """
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
    ]
    rels_root = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>',
        '</Relationships>',
    ]
    workbook_sheets, workbook_rels = [], []
    for idx, (name, _) in enumerate(sheets, start=1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
        workbook_sheets.append(
            f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        )
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
    content_types.append("</Types>")
    rels_root.insert(-1, *workbook_rels)

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets>{"".join(workbook_sheets)}</sheets></workbook>'
    )

    parts = {
        "[Content_Types].xml": "\n".join(content_types).encode("utf-8"),
        "_rels/.rels": "\n".join(rels_root).encode("utf-8"),
        "xl/workbook.xml": workbook_xml.encode("utf-8"),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'{"".join(workbook_rels)}</Relationships>'
        ).encode("utf-8"),
    }

    for idx, (name, rows) in enumerate(sheets, start=1):
        rows_xml = []
        for row_num, cells in rows:
            cell_xml = []
            for ref, value in cells:
                if isinstance(value, str):
                    cell_xml.append(
                        f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(value)}</t></is></c>'
                    )
                else:
                    cell_xml.append(f'<c r="{ref}"><v>{value}</v></c>')
            rows_xml.append(f'<row r="{row_num}">{"".join(cell_xml)}</row>')
        parts[f"xl/worksheets/sheet{idx}.xml"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'<sheetData>{"".join(rows_xml)}</sheetData></worksheet>'
        ).encode("utf-8")

    return parts


def _write_xlsx(path, parts):
    with ZipFile(path, "w") as zf:
        for arcname, data in parts.items():
            zf.writestr(arcname, data, compress_type=ZIP_DEFLATED)


def _ods(sheet_name, rows):
    """Build a minimal OpenDocument spreadsheet in memory (single sheet)."""
    cells_by_row = {}
    for row_num, cells in rows:
        for ref, value in cells:
            if value is None:
                continue
            col = "".join(ch for ch in ref if ch.isalpha())
            row_num = int("".join(ch for ch in ref if ch.isdigit()))
            cells_by_row.setdefault(row_num, {})[col] = value
    rows_xml = []
    for row_num in sorted(cells_by_row):
        cell_xml = []
        for col in sorted(cells_by_row[row_num]):
            value = cells_by_row[row_num][col]
            if isinstance(value, str):
                cell_xml.append(
                    f'<table:table-cell office:value-type="string"><text:p>{escape(value)}</text:p></table:table-cell>'
                )
            else:
                cell_xml.append(
                    f'<table:table-cell office:value-type="float" office:value="{value}"><text:p>{value}</text:p></table:table-cell>'
                )
        rows_xml.append(f'<table:table-row>{"".join(cell_xml)}</table:table-row>')

    content = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" office:version="1.2">'
        "<office:body><office:spreadsheet>"
        f'<table:table table:name="{escape(sheet_name)}">{"".join(rows_xml)}</table:table>'
        "</office:spreadsheet></office:body></office:document-content>"
    )
    meta = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" office:version="1.2">'
        "<office:meta><meta:generator>aspose-cells-cloud-mcp-fixtures</meta:generator></office:meta>"
        "</office:document-meta>"
    )
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">'
        '<manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.spreadsheet"/>'
        '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>'
        '<manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>'
        "</manifest:manifest>"
    )

    def _write(path):
        with ZipFile(path, "w") as zf:
            zf.writestr("mimetype", "application/vnd.oasis.opendocument.spreadsheet", compress_type=ZIP_STORED)
            zf.writestr("content.xml", content.encode("utf-8"), compress_type=ZIP_DEFLATED)
            zf.writestr("meta.xml", meta.encode("utf-8"), compress_type=ZIP_DEFLATED)
            zf.writestr("META-INF/manifest.xml", manifest.encode("utf-8"), compress_type=ZIP_DEFLATED)

    return _write


def _text_cells(rows_data):
    return [(int(row), [(f"{col}{row}", val) for col, val in items]) for row, items in rows_data.items()]


def _book1():
    rows = {
        1: [("A1", "Name"), ("B1", "Value"), ("C1", "Ratio")],
        2: [("A2", "Alpha"), ("B2", 10), ("C2", 0.5)],
        3: [("A3", "Beta"), ("B3", 20), ("C3", 0.75)],
        4: [("A4", "Gamma"), ("B4", 30), ("C4", 1.25)],
        5: [("A5", "Delta"), ("B5", 40), ("C5", 2.0)],
    }
    return [("Sheet1", _text_cells(rows))]


def _booktext():
    rows = {
        1: [("A1", "Text tools fixture")],
        2: [("A2", "data:")],
        4: [("A4", "plain"), ("B4", " spaced "), ("C4", 1234), ("D4", "   Hello  World   \n\n  "), ("E4", "TRAILING  ")],
        5: [("A5", "another")],
        6: [("D6", "    padded")],
        9: [("A9", "last used cell")],
    }
    return [("Text", _text_cells(rows))]


def _booktext_ods(rows):
    return _text_cells(rows)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _write_xlsx(OUT_DIR / "Book1.xlsx", _xlsx(_book1()))
    _write_xlsx(OUT_DIR / "BookText.xlsx", _xlsx(_booktext()))
    ods_rows = {
        1: [("A1", "Text tools fixture")],
        4: [("A4", "plain"), ("B4", " spaced "), ("C4", 1234), ("D4", "   Hello  World   \n\n  "), ("E4", "TRAILING  ")],
        6: [("D6", "    padded")],
    }
    _ods("Text", _text_cells(ods_rows))(OUT_DIR / "BookText.ods")
    print("fixtures written to", OUT_DIR)


if __name__ == "__main__":
    main()
