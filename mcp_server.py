import logging
import os
from fastmcp import FastMCP
from starlette.responses import JSONResponse

import core.convert
import core.io
import core.formats
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

if __name__ == '__main__':
    run_server()