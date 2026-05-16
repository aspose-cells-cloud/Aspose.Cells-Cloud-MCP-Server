import logging
import os
from fastmcp import FastMCP
from starlette.responses import JSONResponse

import core.convert
import core.io
import core.formats
import core.edit
import core.management

mcp = FastMCP('Aspose.Cells Cloud MCP Server')

def _setup_logging():
    level = os.getenv('LOG_LEVEL', '')
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('mcp')

def register_tools() -> None:

    @mcp.tool(description=  "### Get Supported File Load/Import Formats\n"
        "Use this tool to query the list of all source file formats that Aspose.Cells can read (load).\n"
        "Call this tool when a user wants to upload or process a **non-standard Excel file** (e.g., .csv, .json, .xml, .ods, .txt) and you need to verify if the system can parse it.\n\n"
        "### Returns:\n"
        "- **Format Name**: The name of the format (e.g., CSV, JSON, XML, ODS, XLSX, XLS, TXT, HTML).\n"
        "- **Extension**: The file suffix (e.g., .csv, .json).\n"
        "- **Description**: Characteristics of loading this format (e.g., 'Data only, no formatting', 'Requires specific parser', 'Preserves formulas').\n\n"
        "### Usage Guidelines:\n"
        "1. Before calling `upload_file`, if the user is uploading a file with an extension other than .xlsx or .xls, use this tool to confirm the format is recognizable.\n"
        "2. If a user asks 'Can you handle CSV files?', check this list and provide a confirmation.\n"
        "3. Distinguish between 'Load Formats' (Input) and 'Save Formats' (Output). Some formats may support reading but not writing (or vice versa).")
    def list_supported_load_formats():
        """
        Lists all supported load (read) formats and their metadata.
        :return: Return your actual list of Aspose supported load formats here
        """
        return core.formats.list_supported_load_formats()

    @mcp.tool(description= "### Get Supported File Save/Export Formats\n"
        "Use this tool to query the list of all file formats supported by Aspose.Cells for conversion.\n"
        "Call this tool when a user asks to convert an Excel file to another format (e.g., 'convert to PDF', 'save as image', 'export to JSON') and you need to verify the correct file extension or availability.\n\n"
        "### Returns:\n"
        "- **Format Name**: The name of the format (e.g., PDF, HTML, CSV, JSON, XLSX, ODS, TXT, SVG).\n"
        "- **Extension**: The file suffix (e.g., .pdf, .html).\n"
        "- **Description**: A brief explanation of the format's use case (e.g., 'Suitable for printing', 'Web display', 'Programmatic access').\n\n"
        "### 💡 Usage Guidelines:\n"
        "1. Before calling `convert_file` or `convert_with_options`, if you are unsure what string to pass for the `target_format` parameter, use this tool to get the standard extension.\n"
        "2. If a user requests an unsupported format, use this list to recommend the closest available alternative.")
    def list_supported_save_formats():
        """
        Lists all supported save formats and their metadata.
        :return: Return your actual list of Aspose supported formats here
        """
        return core.formats.list_supported_save_formats()

    @mcp.tool(description="Upload file content (provided as a Base64 string) to Aspose Cloud Storage at a specified path.")
    def upload_file(file_content_b64string: str):
        """
        Uploads a file to Aspose Cloud Storage using Base64 encoded content.

        Use this tool when you have file data (e.g., from a conversion result or user upload)
        and need to persist it to the cloud.

        Parameters:
        - file_b64string: The content of the file encoded as a Base64 string. Do not pass a file path here.

        Returns:
        - The file token.
         """
        return core.io.upload_file(file_content_b64string)

    @mcp.tool(description="Download the file identified by the given file token and return its contents as a Base64-encoded string.",)
    def download_file(file_token: str):
        """
        Download the file identified by the given file token and return its contents as a Base64-encoded string.

        Parameters:
        - file_token: The unique identifier of the document.

        Returns:
        - The content of the file encoded as a Base64 string.
         """
        return core.io.download_file(file_token)

    @mcp.tool(description="Convert a spreadsheet in Aspose Cloud Storage to a different format (e.g., XLSX to PDF) and save it as a new file.")
    def save_spreadsheet_as( file_token :str, target_format:str):
        """
         Converts a source spreadsheet to a specified format and saves it to a new path.

         Parameters:
         - file_token: The unique identifier of the document.
         - target_format: The desired output format (e.g., 'PDF', 'CSV', 'XLSX').
        Returns:
        - The file token.
         """
        return core.convert.save_spreadsheet_as(file_token,target_format)

    @mcp.tool(
        description="This tool is specifically designed to handle the printing needs of large-scale data reports. It allows you to enforce specific print scaling strategies when converting spreadsheets into target formats (such as PDF or images). By specifying the scaling mode, you can ensure that the output files strictly conform to the intended page layout, for example, compressing all data onto a single page, or adjusting only the column widths to fit the page width, thereby perfectly addressing issues of content truncation or layout disorder.")
    def get_structure_with_file_token(file_token: str)->str:
        """
        Structurally convert the core metadata, worksheets, tables, pivot tables, charts, shapes, and other information of an Excel workbook into a JObject type JSON object, for scenarios such as data export, API responses, and log recording.
        Parameters:
         - file_token: The unique identifier of the document.
        Returns:
        - The spreadsheet structure.Standard JObject JSON object containing hierarchical structured data: workbook root information, worksheet collection, and nested sub-modules of tables (with column formulas), pivot tables, charts and shape coordinate attributes. Redundant empty nodes are automatically omitted.
         """
        return core.management.get_structure_with_file_token(file_token)

    @mcp.tool(
        description="This tool is specifically designed to handle the printing needs of large-scale data reports. It allows you to enforce specific print scaling strategies when converting spreadsheets into target formats (such as PDF or images). By specifying the scaling mode, you can ensure that the output files strictly conform to the intended page layout, for example, compressing all data onto a single page, or adjusting only the column widths to fit the page width, thereby perfectly addressing issues of content truncation or layout disorder.")
    def get_spreadsheet_structure(spreadsheet_b64string: str) -> str:
        """
        Structurally convert the core metadata, worksheets, tables, pivot tables, charts, shapes, and other information of an Excel workbook into a JObject type JSON object, for scenarios such as data export, API responses, and log recording.
        Parameters:
         - spreadsheet_b64string: The content of the Spreadsheet file (e.g., .xlsx, .ods, .txt, .json, .xml, .xls, and so on) encoded as a Base64 string.
                          Note: Do not pass a file path; the file content must be read and encoded first.
        Returns:
        - The spreadsheet structure.Standard JObject JSON object containing hierarchical structured data: workbook root information, worksheet collection, and nested sub-modules of tables (with column formulas), pivot tables, charts and shape coordinate attributes. Redundant empty nodes are automatically omitted.
         """
        return core.management.get_spreadsheet_structure(spreadsheet_b64string)

    @mcp.tool(
        description="This tool is specifically designed to handle the printing needs of large-scale data reports. It allows you to enforce specific print scaling strategies when converting spreadsheets into target formats (such as PDF or images). By specifying the scaling mode, you can ensure that the output files strictly conform to the intended page layout, for example, compressing all data onto a single page, or adjusting only the column widths to fit the page width, thereby perfectly addressing issues of content truncation or layout disorder.")
    def save_spreadsheet_as_with_scaling_mode(file_token:str ,target_format:str, scaling_mode:str ):
        """
         Converts a source spreadsheet to a specified format and saves it to a new path.
         This tool is specifically designed to handle the printing needs of large-scale data reports. It allows you to enforce specific print scaling strategies when converting spreadsheets into target formats (such as PDF or images). By specifying the scaling mode, you can ensure that the output files strictly conform to the intended page layout, for example, compressing all data onto a single page, or adjusting only the column widths to fit the page width, thereby perfectly addressing issues of content truncation or layout disorder.

         Parameters:
         - file_token: The unique identifier of the document.
         - target_format: The desired output format (e.g., 'PDF', 'CSV', 'XLSX').
         - scaling_mode: NoScaling, FitSheetOnOnePage, FitAllColumnsOnOnePage, FitAllRowsOnOnePage.
            - NoScaling: No scaling. Print according to the actual settings of the worksheet without any automatic adjustments. If the content exceeds the page range, it will be printed on the next page.
            - FitSheetOnOnePage: Adjust the worksheet to one page. Force all rows and columns to scale to fit the width and height of a single sheet of paper.
            - FitAllColumnsOnOnePage: Adjust all columns to fit on one page. Scale all columns to fit the width of one page. The number of rows is not limited and may extend to multiple pages.
            - FitAllRowsOnOnePage: Adjust all rows to fit on one page. Scale all rows to fit the height of one page. The number of columns is not limited and may extend to multiple pages.
        Returns:
        - The file token.
         """
        return core.convert.save_spreadsheet_as_with_scaling_mode(file_token, target_format, scaling_mode)
    @mcp.tool(description="This tool saves spreadsheet data in a specified format and applies custom save options. It allows users to precisely control the behavior of the output file through a JSON object, such as setting passwords, optimizing output, or adjusting rendering properties.")
    def save_spreadsheet_as_with_save_options_json_data( file_token :str, target_format:str,save_options_json_data :str):
        """
         Converts a source spreadsheet to a specified format and saves it to a new path. It allows users to precisely control the behavior of the output file through a JSON object, such as setting passwords, optimizing output, or adjusting rendering properties.

         Parameters:
         - file_token: The unique identifier of the document.
         - target_format: The desired output format (e.g., 'PDF', 'CSV', 'XLSX').
         - save_options_json_data: A JSON-formatted string used to define the specific options for the save operation. For example, you can specify the output format, password protection, whether to embed all fonts, and so on.
        Returns:
        - The file token.
         """
        return core.convert.save_spreadsheet_as_with_save_options_json_data(file_token,target_format,save_options_json_data)
    @mcp.tool(description="Convert Spreadsheet content (provided as a Base64 string) to a specified format such as PDF, CSV, HTML, or XPS.")
    def convert_spreadsheet(spreadsheet_b64string: str, format:str):
        """
       Converts a Spreadsheet file to various other formats.

       This tool accepts the raw content of a Spreadsheet file encoded as a Base64 string
       and a target format string, returning the converted file content.

       Parameters:
       - spreadsheet_b64string: The content of the Spreadsheet file (e.g., .xlsx, .ods, .txt, .json, .xml, .xls, and so on) encoded as a Base64 string.
                          Note: Do not pass a file path; the file content must be read and encoded first.
       - format: The desired output format (e.g., 'PDF', 'CSV', 'HTML', 'XPS', 'ODS').
       """
        return core.convert.convert_spreadsheet( spreadsheet_b64string , format=format )

    @mcp.tool(name="convert_excel_to_pdf", description="Convert an Excel file to PDF. Input must be provided as a Base64 encoded string.")
    def convert_excel_to_pdf(spreadsheet_b64string: str):
        """
        Converts Excel content (XLSX/XLS) to a PDF document.

        This tool accepts the raw file content encoded in Base64 and returns the converted PDF.
        Use this when the user wants to transform a spreadsheet into a non-editable format.

        Parameters:
        - spreadsheet_b64string: The content of the Excel file encoded as a Base64 string.
                           Do not pass a file path; the content must be read and encoded first.
        """
        return core.convert.convert_spreadsheet_to_pdf(spreadsheet_b64string)

    @mcp.tool(name="convert_ods_to_pdf",description="Convert a ODS file to PDF. Input must be provided as a Base64 encoded string.")
    def convert_ods_to_pdf(ods_b64string: str):
        """
        Converts Open Document content (ods) to a PDF document.

        This tool accepts the raw file content encoded in Base64 and returns the converted PDF.
        Use this when the user wants to transform a spreadsheet into a non-editable format.

        Parameters:
        - ods_b64string: The content of the Open Document file encoded as a Base64 string.
                           Do not pass a file path; the content must be read and encoded first.
        """
        return core.convert.convert_spreadsheet_to_pdf(ods_b64string)

    @mcp.tool(name="convert_excel_to_csv",description="Convert Excel content (provided as a Base64 string) to CSV format.")
    def convert_excel_to_csv(spreadsheet_b64string: str):
        """
         Converts an Excel file to CSV format.

         This tool accepts the raw content of an Excel file encoded as a Base64 string
         and returns the converted CSV data (usually as a string or Base64).

         Parameters:
         - spreadsheet_b64string: The content of the Excel file (.xlsx or .xls) encoded as a Base64 string.
                            Note: Do not pass a file path; the file content must be read and encoded first.
         """
        return core.convert.convert_excel_to_csv(spreadsheet_b64string)

    @mcp.tool(name="convert_excel_to_json",description="Convert Excel content (provided as a Base64 string) to JSON format")
    def convert_excel_to_json(spreadsheet_b64string: str):
        """
        Converts an Excel file to JSON format.

        This tool accepts the raw content of an Excel file encoded as a Base64 string
        and returns the converted JSON data representing the spreadsheet rows and columns.

        Parameters:
        - spreadsheet_b64string: The content of the Excel file (.xlsx or .xls) encoded as a Base64 string.
                           Note: Do not pass a file path; the file content must be read and encoded first.
        """
        return core.convert.convert_spreadsheet_to_json(spreadsheet_b64string)

    @mcp.tool(name ="convert_excel",
        description="Convert Excel content (provided as a Base64 string) to a specified format such as PDF, CSV, HTML, or XPS.")
    def convert_excel(spreadsheet_b64string: str, format: str):
        """
       Converts an Excel file to various other formats.

       This tool accepts the raw content of an Excel file encoded as a Base64 string
       and a target format string, returning the converted file content.

       Parameters:
       - spreadsheet_b64string: The content of the Excel file (.xlsx or .xls) encoded as a Base64 string.
                          Note: Do not pass a file path; the file content must be read and encoded first.
       - format: The desired output format (e.g., 'PDF', 'CSV', 'HTML', 'XPS', 'ODS').
       """
        return core.convert.convert_spreadsheet(spreadsheet_b64string, format)

    @mcp.tool(name="trim_text",description="Removes specified leading and trailing characters from text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds."  )
    def trim_text(file_token: str,worksheet:str = None ,_range:str = None,trim_text:str = ' ')->bool:
        """
        Removes specified leading and trailing characters from text values in a given worksheet range. This function uses Aspose.Cells Cloud API to process an Excel file and trim unwanted characters from the beginning and end of each cell's text content within the specified range. It is useful for cleaning data by removing extra spaces, punctuation, or other recurring characters.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param trim_text (str, optional): Character(s) to strip from the beginning of each text cell only. Defaults to a single space character (' ')..
        :return: True if the operation succeeds.
        """
        return core.edit.trim_text(file_token,worksheet,_range,trim_text)

    @mcp.tool(name="trim_text_from_leading",description="Removes specified leading characters only (from the beginning) of text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def trim_text_from_leading(file_token: str,worksheet:str = None ,_range:str = None,trim_text:str = ' ')->bool:
        """
        Removes specified leading characters from the beginning of text values in a worksheet range. This function uses Aspose.Cells Cloud API to process an Excel file and trim unwanted characters only from the start (left side) of each cell's text content. Unlike trim_text(), this does NOT remove trailing characters. It is ideal for cleaning data with consistent prefixes like extra spaces, indentation markers, or special characters at the beginning of cells.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param trim_text (str, optional): Character(s) to strip from the beginning of each text cell only. Defaults to a single space character (' ')..
        :return: True if the operation succeeds.
        """
        return core.edit.trim_text_from_leading(file_token,worksheet,_range,trim_text)

    @mcp.tool(name="trim_text_from_trailing",description="Removes specified trailing characters only (from the end) of text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def trim_text_from_trailing(file_token: str,worksheet:str = None ,_range:str = None,trim_text:str = ' ')->bool:
        """
        Removes specified trailing characters from the beginning of text values in a worksheet range. This function uses Aspose.Cells Cloud API to process an Excel file and trim unwanted characters only from the start (left side) of each cell's text content. Unlike trim_text(), this does NOT remove trailing characters. It is ideal for cleaning data with consistent prefixes like extra spaces, indentation markers, or special characters at the beginning of cells.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param trim_text (str, optional): Character(s) to strip from the beginning of each text cell only. Defaults to a single space character (' ')..
        :return: True if the operation succeeds.
        """
        return core.edit.trim_text_from_trailing(file_token,worksheet,_range,trim_text)

    @mcp.tool(name="remove_extra_line_breaks",description="Removes excessive line breaks (multiple consecutive newline characters) from text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Collapses multiple line breaks into single line breaks or removes them entirely based on configuration. Returns True if the operation succeeds." )
    def remove_extra_line_breaks(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
         Cleans text by removing excessive consecutive line breaks within cells in an Excel worksheet. This function uses Aspose.Cells Cloud API to process an Excel file and normalize line breaks in text cells. It identifies sequences of multiple newline characters (e.g., '\n\n\n', '\r\n\r\n') and reduces them to a single line break, making text more readable and consistent. Leading/trailing line breaks are typically removed entirely.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_extra_line_breaks(file_token,worksheet,_range)

    @mcp.tool(name="remove_all_line_breaks",description="Removes ALL line break characters (including \\n, \\r\\n, \\r) from text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Converts multi-line text into single-line text by deleting all newline characters. Returns True if the operation succeeds." )
    def remove_all_line_breaks(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes ALL line break characters from text cells, converting multi-line text into single-line text. This function uses Aspose.Cells Cloud API to process an Excel file and delete every occurrence of newline characters ('\n', '\r\n', '\r', etc.) from text within cells. Unlike remove_extra_line_breaks() which preserves single line breaks, this function eliminates ALL line breaks, joining previously separate lines into continuous text. Spaces are NOT automatically added; words from different lines will be concatenated directly unless spaces already exist.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_all_line_breaks(file_token,worksheet,_range)

    @mcp.tool(name="word_case",description="Converts text case (uppercase, lowercase, title case, sentence case, or toggle case) within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def word_case(file_token: str,worksheet:str = None ,_range:str = None, word_case_type:str = 'UpperCase')->bool:
        """
        Converts text case within cells using specified transformation rules. This function uses Aspose.Cells Cloud API to process an Excel file and change the case of text values in cells. Supports multiple case conversion types including uppercase, lowercase, title case, sentence case, and toggle case. Ideal for standardizing text formatting across worksheets, preparing data for reports, or cleaning inconsistent capitalization.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param word_case_type (str, optional): Type of case conversion to apply. Must be one of:
                                        - 'UpperCase': Converts all letters to UPPERCASE
                                        - 'LowerCase': Converts all letters to lowercase
                                        - 'TitleCase': Converts to Title Case (Each Major Word Capitalized)
                                        - 'SentenceCase': Converts to Sentence case. (First letter of sentence capitalized)
                                        - 'ToggleCase': Swaps case (Hello → hELLO, World → wORLD)
                                        Defaults to 'UpperCase'.
        :return: True if the operation succeeds.
        """
        return core.edit.word_case(file_token,worksheet,_range,word_case_type)

    @mcp.tool(name="remove_non_printing_characters",description="Removes all non-printing control characters (ASCII 0-31 except tab, newline, carriage return) and other invisible characters from text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def remove_non_printing_characters(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes non-printing control characters and invisible Unicode characters from text cells. This function uses Aspose.Cells Cloud API to process an Excel file and clean text by eliminating non-printing characters that can cause display issues, export problems, or data validation errors. It targets control characters (ASCII 0-31), Unicode control characters, and other invisible formatting marks while preserving standard whitespace (spaces, tabs, newlines, carriage returns).

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_non_printing_characters(file_token,worksheet,_range)

    @mcp.tool(name="remove_text_characters",description="Removes all text/alphabetic characters (A-Z, a-z) from cells within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API, preserving numbers, symbols, and whitespace. Returns True if the operation succeeds." )
    def remove_text_characters(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes all alphabetic characters (A-Z, a-z) from text cells, preserving numbers and symbols. This function uses Aspose.Cells Cloud API to process an Excel file and delete all letter characters from text within cells. It retains numeric digits (0-9), punctuation marks, spaces, symbols, and special characters. This is useful for extracting numeric data, cleaning product codes, isolating identifiers, or preparing data for mathematical operations.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_text_characters(file_token,worksheet,_range)

    @mcp.tool(name="remove_numeric_characters",description="Removes all numeric digit characters (0-9) from cells within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API, preserving letters, symbols, and whitespace. Returns True if the operation succeeds." )
    def remove_numeric_characters(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes all numeric digit characters (0-9) from text cells, preserving letters and symbols. This function uses Aspose.Cells Cloud API to process an Excel file and delete all numeric digits from text within cells. It retains alphabetic characters (A-Z, a-z), punctuation marks, spaces, symbols, and special characters. This is useful for extracting text content, cleaning identifiers, removing order numbers, preparing data for text analysis, or isolating alphabetic codes from mixed alphanumeric data.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_numeric_characters(file_token,worksheet,_range)

    @mcp.tool(name="remove_symbols",description="Removes all symbol and special characters (punctuation, currency symbols, mathematical operators, etc.) from cells within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API, preserving alphanumeric characters (A-Z, a-z, 0-9) and whitespace. Returns True if the operation succeeds." )
    def remove_symbols(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes all symbol and special characters from text cells, preserving only alphanumeric characters and whitespace. This function uses Aspose.Cells Cloud API to process an Excel file and delete all symbol characters from text within cells. It retains only letters (A-Z, a-z), numbers (0-9), and whitespace characters (spaces, tabs, line breaks). All punctuation marks, currency symbols, mathematical operators, brackets, quotes, and other special symbols are removed. This is useful for cleaning text for database storage, creating slugs, generating safe filenames, preparing data for machine learning, or standardizing text for comparison operations.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_symbols(file_token,worksheet,_range)

    @mcp.tool(name="remove_punctuation_marks",description="Removes punctuation marks from text cells while preserving alphanumeric characters and other symbols. This function uses Aspose.Cells Cloud API to process an Excel file and delete punctuation marks from text within cells. It removes sentence-ending punctuation (periods, question marks, exclamation points), internal punctuation (commas, semicolons, colons), quotation marks, apostrophes, parentheses, brackets, and other punctuation. However, it preserves letters (A-Z, a-z), numbers (0-9), spaces, and other symbol characters like currency symbols ($, €, £), mathematical operators (+, -, =, *, /), and special symbols (@, #, %, &, etc.). This is useful for text preprocessing in NLP, removing sentence boundaries for analysis, cleaning text for word counting, or preparing data for text mining where punctuation is considered noise." )
    def remove_punctuation_marks(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes punctuation marks from text cells while preserving alphanumeric characters and other symbols. This function uses Aspose.Cells Cloud API to process an Excel file and delete punctuation marks from text within cells. It removes sentence-ending punctuation (periods, question marks, exclamation points), internal punctuation (commas, semicolons, colons), quotation marks, apostrophes, parentheses, brackets, and other punctuation. However, it preserves letters (A-Z, a-z), numbers (0-9), spaces, and other symbol characters like currency symbols ($, €, £), mathematical operators (+, -, =, *, /), and special symbols (@, #, %, &, etc.). This is useful for text preprocessing in NLP, removing sentence boundaries for analysis, cleaning text for word counting, or preparing data for text mining where punctuation is considered noise.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_punctuation_marks(file_token,worksheet,_range)

    @mcp.tool(name="remove_custom_characters",description="Removes user-specified custom characters from text values within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Supports case-sensitive or case-insensitive removal. Returns True if the operation succeeds." )
    def remove_custom_characters(file_token: str,custom_characters:str, worksheet:str = None ,_range:str = None, case_sensitive:bool = False)->bool:
        """
        Removes user-specified custom characters from text cells with flexible case sensitivity options. This function uses Aspose.Cells Cloud API to process an Excel file and delete all occurrences of specific characters defined by the user. Unlike specialized removal functions (e.g., remove_punctuation_marks, remove_symbols), this function gives complete control over exactly which characters to remove. It can handle single characters, multiple characters, and supports case-sensitive or case-insensitive removal. This is ideal for cleaning data with specific problematic characters, preparing text for legacy systems, removing custom delimiters, or sanitizing input for specific formats.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param custom_characters (str): String containing all characters to be removed. Each character in this string will be individually removed wherever it appears.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param case_sensitive (str, optional): Controls case sensitivity for letter removal. Defaults to False.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_custom_characters(file_token,worksheet,_range,custom_characters,case_sensitive )

    @mcp.tool(name="remove_first_n_characters",description="Removes the first N characters from the beginning of each text cell within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def remove_first_n_characters(file_token: str, number:int,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes the first N characters from the beginning of each text cell in the specified range. This function uses Aspose.Cells Cloud API to process an Excel file and delete a specified number of characters from the start (left side) of each text string within cells. The removal is character-based, counting each character including letters, numbers, symbols, and spaces. This is useful for removing fixed prefixes, area codes, country codes, leading zeros, date prefixes, or any consistent pattern at the beginning of text strings.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param number (int):  Number of characters to remove from the beginning of each text string. Must be a positive integer (1 or greater).If number exceeds the text length, the cell becomes empty.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_first_n_characters(file_token,worksheet,_range, number)

    @mcp.tool(name="remove_last_n_characters",description="Removes the last N characters from the end of each text cell within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def remove_last_n_characters(file_token: str, number:int,worksheet:str = None ,_range:str = None)->bool:
        """
        Removes the last N characters from the end of each text cell in the specified range. This function uses Aspose.Cells Cloud API to process an Excel file and delete a specified number of characters from the end (right side) of each text string within cells. The removal is character-based, counting each character including letters, numbers, symbols, and spaces. This is useful for removing fixed suffixes, file extensions, trailing codes, unit indicators, or any consistent pattern at the end of text strings.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param number (int):  Number of characters to remove from the end of each text string. Must be a positive integer (1 or greater).If number exceeds the text length, the cell becomes empty.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_last_n_characters(file_token,worksheet,_range, number)

    @mcp.tool(name="remove_before_text",description="Removes all characters before (to the left of) a specified delimiter text within each text cell in a worksheet range using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def remove_before_text(file_token: str, text:str, worksheet:str = None ,_range:str = None,  case_sensitive:bool = False)->bool:
        """
        Removes all characters before (to the left of) a specified delimiter text in each text cell. This function uses Aspose.Cells Cloud API to process an Excel file and delete everything that appears before a specific delimiter string within each text cell. The delimiter text itself can be kept as the new beginning of the string or removed. This is useful for extracting data after a specific marker, removing prefixes, cleaning log entries, parsing structured text, or isolating relevant portions of strings.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param text (str): Delimiter text that marks the boundary. All characters before the firstoccurrence of this text (left side) will be removed. If the delimiter is not found, the cell remains unchanged.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param case_sensitive (str, optional): Controls case sensitivity for letter removal. Defaults to False.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_before_text(file_token,worksheet,_range, text,case_sensitive)

    @mcp.tool(name="remove_after_text",description="Removes all characters after (to the right of) a specified delimiter text within each text cell in a worksheet range using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def remove_after_text(file_token: str, text:str, worksheet:str = None ,_range:str = None,  case_sensitive:bool = False)->bool:
        """
        Removes all characters after (to the right of) a specified delimiter text in each text cell. This function uses Aspose.Cells Cloud API to process an Excel file and delete everything that appears before a specific delimiter string within each text cell. The delimiter text itself can be kept as the new beginning of the string or removed. This is useful for extracting data after a specific marker, removing prefixes, cleaning log entries, parsing structured text, or isolating relevant portions of strings.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param text (str): Delimiter text that marks the boundary. All characters after the firstoccurrence of this text (right side) will be removed. If the delimiter is not found, the cell remains unchanged.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :param case_sensitive (str, optional): Controls case sensitivity for letter removal. Defaults to False.
        :return: True if the operation succeeds.
        """
        return core.edit.remove_after_text(file_token,worksheet,_range, text,case_sensitive)

    @mcp.tool(name="add_text_at_head",description="Adds specified text to the beginning (head) of each text cell within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def add_text_at_head(file_token: str, text:str, worksheet:str = None ,_range:str = None)->bool:
        """
        Adds specified text to the beginning (head) of each text cell in the specified range. This function uses Aspose.Cells Cloud API to process an Excel file and prepend a user-specified string to the start of every text cell within the target range. The original cell content is preserved and the new text is added before it. This is useful for adding prefixes, labels, identifiers, formatting markers, or any consistent text that should appear at the beginning of cell values.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param text (str): Text string to be added at the beginning of each cell. Can include letters, numbers, spaces, punctuation, and special characters.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.add_text_at_head(file_token,worksheet,_range, text)

    @mcp.tool(name="add_text_at_tail",description="Adds specified text to the end(tail) of each text cell within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def add_text_at_tail(file_token: str, text:str, worksheet:str = None ,_range:str = None)->bool:
        """
        Adds specified text to the end (tail) of each text cell in the specified range. This function uses Aspose.Cells Cloud API to process an Excel file and prepend a user-specified string to the start of every text cell within the target range. The original cell content is preserved and the new text is added before it. This is useful for adding prefixes, labels, identifiers, formatting markers, or any consistent text that should appear at the beginning of cell values.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param text (str): Text string to be added at the end of each cell. Can include letters, numbers, spaces, punctuation, and special characters.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.add_text_at_tail(file_token,worksheet,_range, text)

    @mcp.tool(name="add_text_before_text",description="Adds specified text immediately before a target delimiter/selector text within each text cell in a worksheet range using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def add_text_before_text(file_token: str, text:str,select_text:str, worksheet:str = None ,_range:str = None)->bool:
        """
        Inserts specified text immediately before a target selector text in each text cell. This function uses Aspose.Cells Cloud API to process an Excel file and insert a user-specified string before the first occurrence of a target selector text within each cell. The original content is preserved, and the new text is added as a prefix to the selector text. This is useful for adding modifiers, prefixes, labels, or additional context before specific markers, delimiters, patterns, or keywords in text data.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param text (str): Text string to be inserted before the target selector text.
        :param select_text (str): Target delimiter or selector text that marks the insertion point. The new text will be placed immediately before the first occurrence of this string.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.add_text_before_text(file_token,worksheet,_range, text,select_text)

    @mcp.tool(name="add_text_after_text",description="Adds specified text immediately after a target delimiter/selector text within each text cell in a worksheet range using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def add_text_after_text(file_token: str, text:str,select_text:str, worksheet:str = None ,_range:str = None)->bool:
        """
        Inserts specified text immediately after a target selector text in each text cell. This function uses Aspose.Cells Cloud API to process an Excel file and insert a user-specified string after the first occurrence of a target selector text within each cell. The original content is preserved, and the new text is added as a suffix to the selector text. This is useful for adding units, modifiers, suffixes, comments, or additional context after specific markers, delimiters, patterns, or keywords in text data.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param text (str): Text string to be inserted after the target selector text.
        :param select_text (str): Target delimiter or selector text that marks the insertion point. The new text will be placed immediately before the first occurrence of this string.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.add_text_after_text(file_token,worksheet,_range, text,select_text)


    @mcp.tool(name="convert_number_to_text",description="Converts numeric values (integers, decimals, percentages, currencies, dates, times) to text strings within a specified range of a worksheet in an Excel file using Aspose.Cells Cloud API. Preserves formatting and converts to user-readable text representation. Returns True if the operation succeeds." )
    def convert_number_to_text(file_token: str,worksheet:str = None ,_range:str = None)->bool:
        """
        Converts numeric values (numbers, dates, times, currencies, percentages) to text strings. This function uses Aspose.Cells Cloud API to process an Excel file and convert numeric cell values to their text representations. This is useful when you need to preserve leading zeros, prevent automatic numeric formatting, prepare data for text-based operations, export data to systems that require text format, or ensure consistent display regardless of locale settings. The conversion respects the cell's number formatting (decimal places, currency symbols, date formats, etc.) and converts the displayed value to a text string.

        :param file_token (str ):  Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.convert_number_to_text(file_token,worksheet,_range)

    @mcp.tool(name="convert_line_break_to_text",description="Replaces all line break characters (\\n, \\r\\n, \\r) within text cells with a specified replacement text string in a worksheet range using Aspose.Cells Cloud API. Returns True if the operation succeeds." )
    def convert_line_break_to_text(file_token: str,target_text:str,worksheet:str = None ,_range:str = None)->bool:
        """
        Replaces all line break characters with a specified replacement text in text cells. This function uses Aspose.Cells Cloud API to process an Excel file and replace all line break characters (newlines, carriage returns, line feeds) within text cells with a user-specified replacement string. This is useful for converting multi-line text to single-line format, preparing data for CSV export, normalizing text for database storage, formatting text for HTML/XML display, or replacing line breaks with custom separators like spaces, commas, orHTML <br> tags.

        :param file_token (str ): Unique token identifying the target Excel file in Aspose.Cells Cloud storage(require).
        :param target_text (str): Replacement text to substitute for line break characters.
        :param worksheet (str, optional): Name of the worksheet (case-sensitive) where the cells reside. If None or empty string, the operation applies to the first worksheet. Defaults to None.
        :param _range (str, optional): Target cell range in standard A1 notation (e.g., "A1:B10") or a named range. Supports single cells, contiguous blocks, or entire columns/rows. If None or empty string, applies to all used (non-empty) cells in the worksheet. Defaults to None.
        :return: True if the operation succeeds.
        """
        return core.edit.convert_line_break_to_text(file_token,worksheet,_range,target_text)

def run_server(transport: str | None=None, host: str='0.0.0.0', port: int=8080, path: str='/mcp', client_id: str | None=None, client_secret: str| None=None) -> None:
    logger = _setup_logging()
    register_tools()
    tr = (transport or os.getenv('MCP_TRANSPORT') or os.getenv('TRANSPORT') or 'stdio').strip().lower()
    logger.info(
        f"Client ID( {os.getenv('ASPOSE_CLOUD_CLIENT_ID')}) and Client Secret ({os.getenv('ASPOSE_CLOUD_CLIENT_SECRET')})")
    if client_id is not None and client_secret is not None:

        os.environ['ASPOSE_CLOUD_CLIENT_ID'] = client_id
        os.environ['ASPOSE_CLOUD_CLIENT_SECRET'] = client_secret

    host_env = (os.getenv('MCP_HOST') or os.getenv('HOST') or host)
    port_env = int(os.getenv('MCP_PORT') or os.getenv('PORT') or port)
    path_http_env = (os.getenv('MCP_PATH') or path)
    path_sse_env = (os.getenv('MCP_SSE_PATH') or '/sse')
    logger.info('Starting Aspose.Cells Cloud MCP Server (FastMCP)...')
    logger.info(f'Transport: %s', tr)
    if tr in {'streamable-http', 'sse'}:
        path_for_tr = path_sse_env if tr == 'sse' else path_http_env
        logger.info('Listening on http://%s:%s%s (%s)', host_env, port_env, path_for_tr, tr)
        mcp.run(transport=tr, host=host_env, port=port_env, path=path_for_tr)
    else:
        mcp.run(transport='stdio')

@mcp.custom_route("/health", methods=["GET"])
async def health_check():
    return JSONResponse({"status": "ok"})
@mcp.custom_route("/version", methods=["GET"])
async def version():
    return JSONResponse({"version": "26.5"})

if __name__ == '__main__':
    run_server()