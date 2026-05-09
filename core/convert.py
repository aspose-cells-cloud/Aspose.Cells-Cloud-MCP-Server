import json

from asposecellscloud.requests import *

from core.formats import get_save_options_with_save_format
from core.utils.spreadsheet_util import *
from asposecellscloud.models import *
import base64
import uuid

from core.utils.spreadsheet_util import get_cells_cloud_client

def save_spreadsheet_as(file_token:str ,target_format:str )->str:
    new_file_path = str(uuid.uuid4())
    save_options_data = SaveOptionsData()
    save_options_data.filename =f"{new_file_path}/File"
    request = SaveSpreadsheetAsRequest( "File", target_format ,save_options_data = save_options_data , folder =file_token )
    response = get_cells_cloud_client().save_spreadsheet_as(request)
    if "OK" == response.status:
        return new_file_path
    else:
        return None

def save_spreadsheet_as_with_scaling_mode(file_token:str ,target_format:str, scaling_mode:str )->str:
    new_file_path = str(uuid.uuid4())
    save_options_data = SaveOptionsData()
    save_options = get_save_options_with_save_format(target_format)
    if scaling_mode != None and save_options != None:
        mode = scaling_mode.lower()
        if mode == "fitsheetononepage":
            save_options.one_page_per_sheet = True
        elif mode == "fitallcolumnsononepage":
            save_options.all_columns_on_one_page = True
        elif mode == "fitallrowsononepage":
            save_options.all_rows_on_one_page = True
        save_options_data.save_options = save_options

    save_options_data.filename = f"{new_file_path}/File"
    request = SaveSpreadsheetAsRequest("File", target_format, save_options_data=save_options_data, folder=file_token)
    response = get_cells_cloud_client().save_spreadsheet_as(request)
    if "OK" == response.status:
        return new_file_path
    else:
        return None

def save_spreadsheet_as_with_save_options_json_data(file_token:str ,target_format:str, save_options_json_data:str )->str:
    new_file_path = str(uuid.uuid4())
    save_options_data = SaveOptionsData()
    save_options = get_save_options_with_save_format(target_format)
    if save_options_json_data != None and save_options != None:
        data = json.loads(save_options_json_data)
        for key, value in data.items():
            if hasattr(save_options, key):
                setattr(save_options, key, value)
        save_options_data.save_options = save_options

    save_options_data.filename = f"{new_file_path}/File"
    request = SaveSpreadsheetAsRequest("File", target_format, save_options_data=save_options_data, folder=file_token)
    response = get_cells_cloud_client().save_spreadsheet_as(request)
    if "OK" == response.status:
        return new_file_path
    else:
        return None

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

