from asposecellscloud import XlsSaveOptions, OoxmlSaveOptions, HtmlSaveOptions, OdsSaveOptions, TxtSaveOptions, \
    XlsbSaveOptions, DifSaveOptions, XmlSaveOptions, MarkdownSaveOptions, XpsSaveOptions, ImageSaveOptions, \
    JsonSaveOptions, DbfSaveOptions, PptxSaveOptions, DocxSaveOptions, PdfSaveOptions, PclSaveOptions, \
    SqlScriptSaveOptions


def list_supported_load_formats():
    return [
        {"format": "CSV", "ext": ".csv","desc": "Comma-separated values, ideal for tabular data exchange. MCP can parse rows/columns."},
        {"format": "XLS", "ext": ".xls","desc": "Legacy Excel 97-2003 binary format. Suitable for older spreadsheets. MCP extracts tables."},
        {"format": "XLSX", "ext": ".xlsx","desc": "Modern Excel format (Office Open XML). Supports macros, formulas, multiple sheets. MCP loads as structured data."},
        {"format": "TSV","ext": ".tsv", "desc": "Tab-separated values, like CSV but with tabs. Useful for clipboard or dataset exports."},
        {"format": "HTML", "ext": ".html","desc": "Web page format. MCP can extract tabular content or readable text from HTML tables/divs."},
        {"format": "MHTML","ext": ".mhtml", "desc": "Single-file web archive (HTML + resources). MCP extracts text/tables."},
        {"format": "XHTML","ext": ".xhtml", "desc": "Rrepesents XHtml file. MCP extracts text/tables."},
        {"format": "ODS","ext": ".ods", "desc": "OpenDocument Spreadsheet (LibreOffice, OpenOffice). MCP reads sheets as tables."},
        {"format": "XLSB","ext": ".xlsb", "desc": "Binary Excel format (fast load/save). MCP decodes sheets."},
        {"format": "DIF","ext": ".dif", "desc": "Data Interchange Format, old but standard. MCP supports basic table conversion."},
        {"format": "OTS", "ext": ".ots","desc": "OpenDocument spreadsheet template. MCP reads similar to ODS."},
        {"format": "XML","ext": ".xml", "desc": "Generic XML file. MCP parses structured data or converts to tabular if possible."},
        {"format": "EPUB","ext": ".epub", "desc": "E-book format. MCP extracts plain text and basic metadata."},
        {"format": "AZW3","ext": ".azw3", "desc": "Kindle e-book format (Amazon). MCP extracts readable text."},
        {"format": "CHM", "ext": ".chm","desc": "Compiled HTML Help (Windows). MCP extracts text and topics."},
        {"format": "MARKDOWN","ext": ".md", "desc": "Lightweight markup. MCP converts to plain text, retains structure for LLM use."},
        {"format": "NUMBERS","ext": ".number", "desc": "Apple Numbers spreadsheet. MCP reads tables and sheets."},
        {"format": "FODS","ext": ".fods", "desc": "OpenDocument Flat XML Spreadsheet — human-readable XML. MCP processes as sheet data."},
        {"format": "SXC", "ext": ".sxc","desc": "StarOffice Calc legacy format. MCP supports tabular extraction."},
        {"format": "IMAGE","ext": ".jpg,.png,.bmp,.svg,.tiff", "desc": "Image file (PNG, JPEG, etc.). MCP OCR or metadata extraction depends on server capabilities."},
        {"format": "JSON","ext": ".json", "desc": "JSON structured data. MCP loads directly as object/array, ideal for API-like data."},
        {"format": "DBF","ext": ".dbf", "desc": "Xbase database file (dBase, FoxPro). MCP reads rows/columns as table."},
    ]
def list_supported_save_formats():
    return [
        {"format": "CSV", "ext": ".csv","desc": "Comma-separated values, ideal for tabular data exchange. MCP can parse rows/columns."},
        {"format": "XLS","ext": ".xls", "desc": "Legacy Excel 97-2003 binary format. Suitable for older spreadsheets. MCP extracts tables."},
        {"format": "XLSX","ext": ".xlsx", "desc": "Modern Excel format (Office Open XML). Supports macros, formulas, multiple sheets. MCP loads as structured data."},
        {"format": "TSV","ext": ".tsv", "desc": "Tab-separated values, like CSV but with tabs. Useful for clipboard or dataset exports."},
        {"format": "HTML", "ext": ".html","desc": "Web page format. MCP can extract tabular content or readable text from HTML tables/divs."},
        {"format": "MHTML", "ext": ".mhtml","desc": "Single-file web archive (HTML + resources). MCP extracts text/tables."},
        {"format": "ODS","ext": ".ods", "desc": "OpenDocument Spreadsheet (LibreOffice, OpenOffice). MCP reads sheets as tables."},
        {"format": "XLSB", "ext": ".xlsb","desc": "Binary Excel format (fast load/save). MCP decodes sheets."},
        {"format": "DIF", "ext": ".dif","desc": "Data Interchange Format, old but standard. MCP supports basic table conversion."},
        {"format": "OTS", "ext": ".ots","desc": "OpenDocument spreadsheet template. MCP reads similar to ODS."},
        {"format": "XML", "ext": ".xml","desc": "Generic XML file. MCP parses structured data or converts to tabular if possible."},
        {"format": "EPUB","ext": ".epub", "desc": "E-book format. MCP extracts plain text and basic metadata."},
        {"format": "AZW3", "ext": ".azw3","desc": "Kindle e-book format (Amazon). MCP extracts readable text."},
        {"format": "CHM", "ext": ".chm","desc": "Compiled HTML Help (Windows). MCP extracts text and topics."},
        {"format": "MARKDOWN","ext": ".md", "desc": "Lightweight markup. MCP converts to plain text, retains structure for LLM use."},
        {"format": "NUMBERS", "ext": ".numbers","desc": "Apple Numbers spreadsheet. MCP reads tables and sheets."},
        {"format": "FODS","ext": ".fods", "desc": "OpenDocument Flat XML Spreadsheet — human-readable XML. MCP processes as sheet data."},
        {"format": "SXC","ext": ".sxc", "desc": "StarOffice Calc legacy format. MCP supports tabular extraction."},
        {"format": "XPS", "ext": ".xps","desc": "XPS (XML Paper Specification) format."},
        {"format": "TIFF","ext": ".tiff","desc": "Represents a TIFF file."},
        {"format": "SVG", "ext": ".svg","desc": "Represents a SVG file."},
        {"format": "EMF","ext": ".emf", "desc": " Windows Enhanced Metafile.."},
        {"format": "JPG", "ext": ".jpg","desc": "Represents a JPEG file."},
        {"format": "PNG","ext": ".png","desc": "Represents Portable Network Graphics."},
        {"format": "BMP","ext": ".bmp", "desc": "Represents a Windows Bitmap file."},
        {"format": "GIF", "ext": ".gif","desc": "Represents a Gif file."},
        {"format": "JSON","ext": ".json", "desc": "JSON structured data. MCP loads directly as object/array, ideal for API-like data."},
        {"format": "DBF","ext": ".dbf", "desc": "Xbase database file (dBase, FoxPro). MCP reads rows/columns as table."},
        {"format": "PPTX","ext": ".pptx", "desc": "Represents .pptx file."},
        {"format": "DOCX", "ext": ".docx","desc": "Represents .docx file."},
        {"format": "PDF", "ext": ".pdf","desc": "Represents a Pdf file."},
        {"format": "XLTX","ext": ".xltx", "desc": "Represents a xltx file."},
        {"format": "XLSM","ext": ".xlsm", "desc": "Represents a xlsm file which enable macros."},
        {"format": "SQL", "ext": ".sql", "desc": "Represents a sql file."},
        {"format": "PCL", "ext": ".pcl", "desc": "Represents a pcl file."},
    ]
def get_save_options_with_save_format( save_format :str ):
    format = save_format.lower()
    if format == "csv":
        return TxtSaveOptions()
    elif format == "xls":
        return XlsSaveOptions()
    elif format == "xlsx":
        return OoxmlSaveOptions(save_format=save_format)
    elif format == "tsv":
        return TxtSaveOptions()
    elif format == "html":
        return HtmlSaveOptions( save_format )
    elif format == "mhtml":
        return HtmlSaveOptions( save_format )
    elif format == "ods":
        return OdsSaveOptions( save_format= save_format )
    elif format == "xlsb":
        return XlsbSaveOptions( save_format )
    elif format == "dif":
        return DifSaveOptions( save_format )
    elif format == "ots":
        return OdsSaveOptions( save_format= save_format )
    elif format == "xml":
        return XmlSaveOptions( )
    elif format == "epub":
        return HtmlSaveOptions( save_format= save_format )
    elif format == "azw3":
        return None
    elif format == "chm":
        return None
    elif format == "markdown":
        return MarkdownSaveOptions()
    elif format == "numbers":
        return OoxmlSaveOptions(save_format=save_format)
    elif format == "fods":
        return OdsSaveOptions(save_format=save_format)
    elif format == "sxc":
        return None
    elif format == "xps":
        return XpsSaveOptions()
    elif format == "tiff":
        return ImageSaveOptions(image_format=save_format)
    elif format == "svg":
        return ImageSaveOptions(image_format=save_format)
    elif format == "emf":
        return ImageSaveOptions(image_format=save_format)
    elif format == "jpg":
        return ImageSaveOptions(image_format=save_format)
    elif format == "png":
        return ImageSaveOptions(image_format=save_format)
    elif format == "bmp":
        return ImageSaveOptions(image_format=save_format)
    elif format == "gif":
        return ImageSaveOptions(image_format=save_format)
    elif format == "json":
        return JsonSaveOptions()
    elif format == "dbf":
        return DbfSaveOptions()
    elif format == "pptx":
        return PptxSaveOptions()
    elif format == "docx":
        return DocxSaveOptions
    elif format == "pdf":
        return PdfSaveOptions
    elif format == "xltx":
        return OoxmlSaveOptions(save_format=save_format)
    elif format == "xlsm":
        return OoxmlSaveOptions(save_format=save_format)
    elif format == "sql":
        return SqlScriptSaveOptions()
    elif format == "pcl":
        return PclSaveOptions()
    else:
        return  None