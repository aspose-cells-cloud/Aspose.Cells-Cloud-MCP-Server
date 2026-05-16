import uuid
import json

from asposecellscloud import TrimCharacterInRemoteSpreadsheetRequest,UpdateWordCaseInRemoteSpreadsheetRequest,RemoveCharactersInRemoteSpreadsheetRequest,RemoveCharactersByPositionInRemoteSpreadsheetRequest,AddTextInRemoteSpreadsheetRequest,ConvertTextInRemoteSpreadsheetRequest,GetStructureInRemoteSpreadsheetRequest

from core.utils.spreadsheet_util import get_cells_cloud_client,num_to_cell


def trim_text(file_token:str,worksheet:str,_range:str ,trim_text:str = ' ')->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        if trim_text == ' ':
            request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range, trim_leading=True,
                                                            trim_trailing=True, folder=file_token)
        else:
            request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range, trim_content=trim_text,
                                                            trim_leading=True, trim_trailing=True, folder=file_token)

        response = get_cells_cloud_client().trim_character_in_remote_spreadsheet(request)
        if response.status != "OK":
            result = False
    return result

def trim_text_from_leading(file_token:str,worksheet:str,_range:str ,trim_text:str = ' ')->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        if trim_text == ' ':
            request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range,
                                                            trim_leading=True, folder=file_token)
        else:
            request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range, trim_content=trim_text,
                                                            trim_leading=True, folder=file_token)
        response = get_cells_cloud_client().trim_character_in_remote_spreadsheet(request)
        if response.status != "OK":
            result = False
    return result

def trim_text_from_trailing(file_token:str,worksheet:str,_range:str ,trim_text:str = ' ')->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        if trim_text == ' ':
            request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range,
                                                            trim_trailing=True, folder=file_token)
        else:
            request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range, trim_content=trim_text,
                                                            trim_trailing=True, folder=file_token)
        response = get_cells_cloud_client().trim_character_in_remote_spreadsheet(request)
        if response.status != "OK":
            result = False
    return result

def remove_extra_line_breaks(file_token:str,worksheet:str,_range:str )->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range,
                                                        remove_extra_line_breaks =True, folder=file_token)
        response = get_cells_cloud_client().trim_character_in_remote_spreadsheet(request)
        if response.status != "OK":
            result = False
    return result

def remove_all_line_breaks(file_token:str,worksheet:str,_range:str )->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        request = TrimCharacterInRemoteSpreadsheetRequest("File", worksheet, new_range,
                                                        remove_all_line_breaks =True, folder=file_token)
        response = get_cells_cloud_client().trim_character_in_remote_spreadsheet(request)
        if response.status != "OK":
            result = False
    return result

def word_case(file_token:str,worksheet:str,_range:str, word_case_type:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        response = get_cells_cloud_client().update_word_case_in_remote_spreadsheet(
            UpdateWordCaseInRemoteSpreadsheetRequest("File", worksheet, new_range, word_case_type, folder=file_token))
        if response.status != "OK":
            result = False
    return result 

def remove_non_printing_characters(file_token:str,worksheet:str,_range:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersInRemoteSpreadsheetRequest("File", worksheet, new_range, remove_text_method="RemoveCharacterSets",
                                                    character_sets="NonPrintingCharacters", folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_text_characters(file_token:str,worksheet:str,_range:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersInRemoteSpreadsheetRequest("File", worksheet, new_range, remove_text_method="RemoveCharacterSets",
                                                    character_sets="TextCharacters", folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_numeric_characters(file_token:str,worksheet:str,_range:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersInRemoteSpreadsheetRequest("File", worksheet, new_range, remove_text_method="RemoveCharacterSets",
                                                    character_sets="NumericCharacters", folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_symbols(file_token:str,worksheet:str,_range:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersInRemoteSpreadsheetRequest("File", worksheet, new_range, remove_text_method="RemoveCharacterSets",
                                                       character_sets="Symbols", folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_punctuation_marks(file_token:str,worksheet:str,_range:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersInRemoteSpreadsheetRequest("File", worksheet, new_range, remove_text_method="RemoveCharacterSets",
                                                    character_sets="PunctuationMarks", folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_custom_characters(file_token:str,worksheet:str,_range:str,custom_characters:str,  case_sensitive:bool = False)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersInRemoteSpreadsheetRequest("File", worksheet, new_range,
                                                    remove_text_method="RemoveCustomCharacter",
                                                    remove_custom_value=custom_characters, case_sensitive=case_sensitive,
                                                    folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_first_n_characters(file_token:str,worksheet:str,_range:str, number:int)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
  
        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersByPositionInRemoteSpreadsheetRequest("File", worksheet, new_range, the_first_n_characters=number,
                                                             folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_last_n_characters(file_token:str,worksheet:str,_range:str, number:int)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"    

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersByPositionInRemoteSpreadsheetRequest("File", worksheet, new_range, the_last_n_characters=number,
                                                                folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_before_text(file_token:str,worksheet:str,_range:str, text:str,  case_sensitive:bool = False)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersByPositionInRemoteSpreadsheetRequest("File", worksheet, new_range, all_characters_before_text=text,
                                                                case_sensitive=case_sensitive,folder=file_token))
        if response.status != "OK":
            result = False
    return result

def remove_after_text(file_token:str,worksheet:str,_range:str, text:str,  case_sensitive:bool = False)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    

        response = get_cells_cloud_client().remove_characters_in_remote_spreadsheet(
            RemoveCharactersByPositionInRemoteSpreadsheetRequest("File", worksheet, new_range,all_characters_before_text=text,
                                                                case_sensitive=case_sensitive,folder=file_token))
        if response.status != "OK":
            result = False
    return result

def add_text_at_head(file_token:str,worksheet:str,_range:str, text:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().add_text_in_remote_spreadsheet(
            AddTextInRemoteSpreadsheetRequest("File", worksheet, new_range, text,"AtTheBeginning",folder=file_token))
        if response.status != "OK":
            result = False
    return result

def add_text_at_tail(file_token:str,worksheet:str,_range:str, text:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().add_text_in_remote_spreadsheet(
            AddTextInRemoteSpreadsheetRequest("File", worksheet, new_range, text,"AtTheEnd",folder=file_token))
        if response.status != "OK":
            result = False
    return result

def add_text_before_text(file_token:str,worksheet:str,_range:str, text:str,select_text:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().add_text_in_remote_spreadsheet(
            AddTextInRemoteSpreadsheetRequest("File", worksheet, new_range, text,"BeforeText", select_text=select_text,folder=file_token))
        if response.status != "OK":
            result = False
    return result 

def add_text_after_text(file_token:str,worksheet:str,_range:str, text:str,select_text:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().add_text_in_remote_spreadsheet(
            AddTextInRemoteSpreadsheetRequest("File", worksheet, new_range, text,"AfterText", select_text=select_text,folder=file_token))
        if response.status != "OK":
            result = False
    return result            

def convert_number_to_text(file_token:str,worksheet:str,_range:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().convert_text_in_remote_spreadsheet(
            ConvertTextInRemoteSpreadsheetRequest("File", worksheet, new_range,convert_text_type= "ConvertNumberToText",folder=file_token))
        if response.status != "OK":
            result = False
    return result

def convert_line_break_to_text(file_token:str,worksheet:str,_range:str,target_text:str)->bool:
    result = True
    strcuture = get_cells_cloud_client().get_structure_in_remote_spreadsheet( GetStructureInRemoteSpreadsheetRequest("File",folder = file_token))    
    strcuture_json = json.loads(strcuture)
    for worksheet_json in strcuture_json["Worksheets"]:
        if ( worksheet is not None or worksheet != "" ) and worksheet != worksheet_json["Name"]:
            continue
        new_range = _range
        if _range is None or worksheet == "":
            new_range = f"A1:{num_to_cell(worksheet_json['MaxDataRow'],worksheet_json['MaxDataColumn'])}"
    
        response = get_cells_cloud_client().convert_text_in_remote_spreadsheet(
            ConvertTextInRemoteSpreadsheetRequest("File", worksheet, new_range,convert_text_type= "ConvertLinebreak",target_characters= target_text,folder=file_token))
        if response.status != "OK":
            result = False
    return result

