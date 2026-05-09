import base64

from core.utils.spreadsheet_util import get_cells_cloud_client
from asposecellscloud.requests import *
def get_structure_with_file_token( file_token:str) ->str:
    request = GetStructureInRemoteSpreadsheetRequest("File" ,folder = file_token)
    return get_cells_cloud_client().get_structure_in_remote_spreadsheet(request)

def get_spreadsheet_structure( spreadsheet_b64string :str ) ->str:
    request = GetSpreadsheetStructureRequest(  base64.b64decode( spreadsheet_b64string.strip()) )
    return get_cells_cloud_client().get_spreadsheet_structure(request)