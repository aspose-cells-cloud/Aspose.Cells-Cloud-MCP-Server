import logging
import os
from fastmcp import FastMCP

import core.convert

mcp = FastMCP('Aspose.Cells Cloud MCP Server')

def _setup_logging():
    level = os.getenv('LOG_LEVEL', '')
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('mcp')

def register_tools() -> None:
    @mcp.tool(description="Upload file content (provided as a Base64 string) to Aspose Cloud Storage at a specified path.")
    def upload_file(file_b64string: str, file_path :str,storage_name:str =None):
        """
        Uploads a file to Aspose Cloud Storage using Base64 encoded content.

        Use this tool when you have file data (e.g., from a conversion result or user upload)
        and need to persist it to the cloud.

        Parameters:
        - file_b64string: The content of the file encoded as a Base64 string. Do not pass a file path here.
        - file_path: The destination path in the cloud storage where the file will be saved (e.g., '/folder/filename.pdf').
        - storage_name: (Optional) The name of the storage.

        Returns:
        - The storage path of the successfully uploaded file.
         """
        return core.io.upload_file(file_b64string,file_path,storage_name)

    @mcp.tool(description="Convert a spreadsheet in Aspose Cloud Storage to a different format (e.g., XLSX to PDF) and save it as a new file.")
    def save_spreadsheet_as( filename :str, target_format:str,target_file_path:str , folder: str= None, storage_name:str =None):
        """
         Converts a source spreadsheet to a specified format and saves it to a new path.

         Parameters:
         - filename: The name of the source file (e.g., 'data.xlsx').
         - target_format: The desired output format (e.g., 'PDF', 'CSV', 'XLSX').
         - target_file_path: The full path where the converted file should be saved (e.g., '/converted/data.pdf').
         - folder: (Optional) The folder path of the source file.
         - storage_name: (Optional) The name of the storage.
         """
        return core.io.save_spreadsheet_as(filename,target_format,target_file_path,folder,storage_name)

    @mcp.tool(description="Convert Spreadsheet content (provided as a Base64 string) to a specified format such as PDF, CSV, HTML, or XPS.")
    def convert_spreadsheet(excel_b64string: str, format:str):
        """
       Converts a Spreadsheet file to various other formats.

       This tool accepts the raw content of a Spreadsheet file encoded as a Base64 string
       and a target format string, returning the converted file content.

       Parameters:
       - excel_b64string: The content of the Spreadsheet file (e.g., .xlsx, .ods, .txt, .json, .xml, .xls, and so on) encoded as a Base64 string.
                          Note: Do not pass a file path; the file content must be read and encoded first.
       - format: The desired output format (e.g., 'PDF', 'CSV', 'HTML', 'XPS', 'ODS').
       """
        return core.convert.convert_spreadsheet( excel_b64string , format=format )

    @mcp.tool(name="convert_excel_to_pdf", description="Convert an Excel file to PDF. Input must be provided as a Base64 encoded string.")
    def convert_excel_to_pdf(excel_b64string: str):
        """
        Converts Excel content (XLSX/XLS) to a PDF document.

        This tool accepts the raw file content encoded in Base64 and returns the converted PDF.
        Use this when the user wants to transform a spreadsheet into a non-editable format.

        Parameters:
        - excel_b64string: The content of the Excel file encoded as a Base64 string.
                           Do not pass a file path; the content must be read and encoded first.
        """
        return convert_spreadsheet(excel_b64string, format = 'pdf')

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
        return convert_spreadsheet(ods_b64string,"pdf")

    @mcp.tool(name="convert_excel_to_csv",description="Convert Excel content (provided as a Base64 string) to CSV format.")
    def convert_excel_to_csv(excel_b64string: str):
        """
         Converts an Excel file to CSV format.

         This tool accepts the raw content of an Excel file encoded as a Base64 string
         and returns the converted CSV data (usually as a string or Base64).

         Parameters:
         - excel_b64string: The content of the Excel file (.xlsx or .xls) encoded as a Base64 string.
                            Note: Do not pass a file path; the file content must be read and encoded first.
         """
        return convert_spreadsheet(excel_b64string,  'csv')

    @mcp.tool(name="convert_excel_to_json",description="Convert Excel content (provided as a Base64 string) to JSON format")
    def convert_excel_to_json(excel_b64string: str):
        """
        Converts an Excel file to JSON format.

        This tool accepts the raw content of an Excel file encoded as a Base64 string
        and returns the converted JSON data representing the spreadsheet rows and columns.

        Parameters:
        - excel_b64string: The content of the Excel file (.xlsx or .xls) encoded as a Base64 string.
                           Note: Do not pass a file path; the file content must be read and encoded first.
        """
        return convert_spreadsheet(excel_b64string,"json")

    @mcp.tool(name ="convert_excel",
        description="Convert Excel content (provided as a Base64 string) to a specified format such as PDF, CSV, HTML, or XPS.")
    def convert_excel(excel_b64string: str, format: str):
        """
       Converts an Excel file to various other formats.

       This tool accepts the raw content of an Excel file encoded as a Base64 string
       and a target format string, returning the converted file content.

       Parameters:
       - excel_b64string: The content of the Excel file (.xlsx or .xls) encoded as a Base64 string.
                          Note: Do not pass a file path; the file content must be read and encoded first.
       - format: The desired output format (e.g., 'PDF', 'CSV', 'HTML', 'XPS', 'ODS').
       """
        return convert_spreadsheet(excel_b64string, format)
    
def run_server(transport: str | None=None, host: str='0.0.0.0', port: int=8080, path: str='/mcp', client_id: str | None=None, client_secret: str| None=None) -> None:
    logger = _setup_logging()
    register_tools()
    tr = (transport or os.getenv('MCP_TRANSPORT') or os.getenv('TRANSPORT') or 'stdio').strip().lower()
    if client_id is not None and client_secret is not None:
        logger.info(f"Client ID( {client_id}) and Client Secret ({client_secret})")
        os.environ['ASPOSE_CLOUD_CLIENT_ID'] = client_id
        os.environ['ASPOSE_CLOUD_SECRET_KEY'] = client_secret

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

if __name__ == '__main__':
    run_server()