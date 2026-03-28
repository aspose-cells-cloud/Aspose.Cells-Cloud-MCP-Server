import logging
import os
import FastMCP

import core.convert

mcp = FastMCP('Aspose.Cells Cloud MCP Server')

def _setup_logging():
    level = os.getenv('LOG_LEVEL', '')
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('mcp')



def register_tools() -> None:
    @mcp.tool(description="Upload a file to Aspose Cloud Storage. Returns the storage path or file identifier upon successful upload.")
    def upload_file(file_b64string: str, file_path :str,storage_name:str =None):
        return core.io.upload_file(file_b64string,file_path,storage_name)
    pass

    @mcp.tool(description="Upload a file to Aspose Cloud Storage. Returns the storage path or file identifier upon successful upload.")
    def save_spreadsheet_as( filename :str, target_format:str,target_file_path:str , folder: str= None, storage_name:str =None):
        return core.io.save_spreadsheet_as(filename,target_format,target_file_path,folder,storage_name)
    pass

    @mcp.tool(description="Convert a local Excel file to a pdf file.")
    def convert_local_excel_to_pdf(excel_b64string: str):
        return core.convert.convert_spreadsheet_to_pdf( excel_b64string )
    pass

    @mcp.tool(description="Convert a local ODS file to a pdf file.")
    def convert_local_ods_to_pdf(ods_b64string: str):
        return core.convert.convert_spreadsheet_to_pdf( ods_b64string )
    pass

    @mcp.tool(description="Convert a local Excel file to a csv file.")
    def convert_local_excel_to_csv(excel_b64string: str):
        return core.convert.convert_spreadsheet_to_csv( excel_b64string )
    pass

    @mcp.tool(description="Convert a local Excel file to a json file.")
    def convert_local_excel_to_json(excel_b64string: str):
        return core.convert.convert_spreadsheet_to_json( excel_b64string )
    pass
    @mcp.tool(description=" Convert a local Excel file to a different file format. Supports various output formats including CSV, PDF, HTML, and more.")
    def convert_local_excel(excel_b64string: str, format:str):
        return core.convert.convert_spreadsheet( excel_b64string , format=format )
    pass
def run_server(transport: str | None=None, host: str='0.0.0.0', port: int=8080, path: str='/mcp', client_id: str | None=None, client_secret: str| None=None) -> None:
    logger = _setup_logging()
    register_tools()
    tr = (transport or os.getenv('MCP_TRANSPORT') or os.getenv('TRANSPORT') or 'stdio').strip().lower()
    if client_id is not None and client_secret is not None:
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