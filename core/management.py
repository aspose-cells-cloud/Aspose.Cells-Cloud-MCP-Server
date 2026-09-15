import base64

from asposecellscloud.requests import GetSpreadsheetStructureRequest, GetStructureInRemoteSpreadsheetRequest

from core import storage
from core.utils.spreadsheet_util import get_cells_cloud_client


def get_structure_with_file_uuid(file_uuid: str) -> str:
    handle = storage.resolve(file_uuid)
    request = GetStructureInRemoteSpreadsheetRequest(handle["name"], folder=handle["folder"])
    return get_cells_cloud_client().get_structure_in_remote_spreadsheet(request)


def get_spreadsheet_structure(spreadsheet_b64string: str) -> str:
    request = GetSpreadsheetStructureRequest(base64.b64decode(spreadsheet_b64string.strip()))
    return get_cells_cloud_client().get_spreadsheet_structure(request)
