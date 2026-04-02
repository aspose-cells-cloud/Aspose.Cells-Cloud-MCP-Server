import os
from asposecellscloud.requests import *
from asposecellscloud.apis import  *
import base64

from core.utils.spreadsheet_util import get_cells_cloud_client

def convert_spreadsheet_to_pdf( spreadsheet_b64string :str  )  -> str:
    request = ConvertSpreadsheetToPdfRequest( base64.b64decode( spreadsheet_b64string.strip()) )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_pdf( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    os.remove(temp_file_path)
    return  base64.b64encode(file_bytes)

def convert_spreadsheet_to_html(  spreadsheet_b64string :str ) -> str:
    request = ConvertSpreadsheetRequest( base64.b64decode( spreadsheet_b64string.strip()),"html" )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    os.remove(temp_file_path)
    return  base64.b64encode(file_bytes)

def convert_excel_to_csv(  spreadsheet_b64string :str ) -> str:
    request = ConvertSpreadsheetToCsvRequest( base64.b64decode( spreadsheet_b64string.strip()) )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_csv( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    os.remove(temp_file_path)
    return  base64.b64encode(file_bytes)

def convert_spreadsheet_to_json(  spreadsheet_b64string :str ) -> str:
    request = ConvertSpreadsheetToJsonRequest( base64.b64decode( spreadsheet_b64string.strip()) )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_json( request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    os.remove(temp_file_path)
    return  base64.b64encode(file_bytes)

def convert_spreadsheet( spreadsheet_b64string :str , format:str) ->str:
    request =  ConvertSpreadsheetRequest( base64.b64decode( spreadsheet_b64string), format=format )
    temp_file_path = get_cells_cloud_client().convert_spreadsheet(request)
    with open(temp_file_path, "rb") as file:
        file_bytes = file.read()
    os.remove(temp_file_path)
    return  base64.b64encode(file_bytes)

