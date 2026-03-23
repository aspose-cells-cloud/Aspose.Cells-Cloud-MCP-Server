import os
from asposecellscloud.requests import *
from utils.spreadsheet_util import *
import base64


def convert_spreadsheet_to_pdf( file_content_b64string :str  )  -> str:
    request = ConvertSpreadsheetToPdfRequest( base64.b64decode( file_content_b64string.strip()) )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_pdf( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    return  base64.b64encode(file_bytes)

def convert_spreadsheet_to_html( cells_cloud_client : CellsApi, file_content_b64string :str ) -> str:
    request = ConvertSpreadsheetRequest( base64.b64decode( file_content_b64string.strip()),"html" )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    return  base64.b64encode(file_bytes)

def convert_spreadsheet_to_csv( cells_cloud_client : CellsApi, file_content_b64string :str ) -> str:
    request = ConvertSpreadsheetToCsvRequest( base64.b64decode( file_content_b64string.strip()) )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_csv( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    return  base64.b64encode(file_bytes)

def convert_spreadsheet_to_json( cells_cloud_client : CellsApi, file_content_b64string :str ) -> str:
    request = ConvertSpreadsheetToJsonRequest( base64.b64decode( file_content_b64string.strip()) )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_json( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    return  base64.b64encode(file_bytes)

def convert_spreadsheet( cells_cloud_client :CellsApi, file_content_b64string :str , format:str) ->str:
    request =  ConvertSpreadsheetRequest( base64.b64decode( file_content_b64string), format=format )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet(request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    return  base64.b64encode(file_bytes)

