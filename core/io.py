from utils.spreadsheet_util import *
from asposecellscloud.requests import *
from asposecellscloud.models import *
import base64


def upload_file(file_content_b64string:str, file_path :str,storage_name:str =None):
    request = UploadFileRequest( base64.b64decode( file_content_b64string.strip()) , file_path ,storage_name)
    get_cells_cloud_client().upload_file(request)

def create_spreadsheet(spreadsheet_name:str ,format:str, folder:str, storage_name :str =None  ):
    path = folder.repace("\\","/")
    if not path.endswith('/'):
        path = path + '/'
    path = path +spreadsheet_name
    request = CreateSpreadsheetRequest(format , None, path,storage_name)
    get_cells_cloud_client().create_spreadsheet(request)

def save_spreadsheet_as(spreadsheet_name:str ,format:str, save_path:str = None ,folder:str=None ,storage_name :str =None ):
    request = SaveSpreadsheetAsRequest( spreadsheet_name, format)
    if save_path is not None:
        save_options_data = SaveOptionsData()
        save_options_data.filename = save_path
        request.save_options_data = save_options_data
    get_cells_cloud_client().save_spreadsheet_as(request)