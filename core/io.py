from asposecellscloud import UploadFileRequest, CreateSpreadsheetRequest, SaveSpreadsheetAsRequest, DownloadFileRequest
import uuid
from core.utils.spreadsheet_util import *
import base64

def upload_file(file_content_b64string:str) -> str:
    file_path = str( uuid.uuid4())
    request = UploadFileRequest( base64.b64decode( file_content_b64string.strip()) , file_path)
    response =  get_cells_cloud_client().upload_file(request)
    return file_path

def download_file(file_token:str) -> str:
    request = DownloadFileRequest( file_token +"/File" )
    temp_path = get_cells_cloud_client().download_file(request)
    with open(temp_path, 'rb') as file:
        file_content = file.read()
    os.remove(temp_path)
    return base64.b64encode(file_content).decode('utf-8')
def create_spreadsheet(spreadsheet_name:str ,format:str, folder:str, storage_name :str =None  ):
    path = folder.repace("\\","/")
    if not path.endswith('/'):
        path = path + '/'
    path = path +spreadsheet_name
    request = CreateSpreadsheetRequest(format , None, path,storage_name)
    get_cells_cloud_client().create_spreadsheet(request)

