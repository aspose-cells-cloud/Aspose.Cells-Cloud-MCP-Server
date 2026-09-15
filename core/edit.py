import json

from asposecellscloud.requests import (
    AddTextInRemoteSpreadsheetRequest,
    ConvertTextInRemoteSpreadsheetRequest,
    GetStructureInRemoteSpreadsheetRequest,
    RemoveCharactersByPositionInRemoteSpreadsheetRequest,
    RemoveCharactersInRemoteSpreadsheetRequest,
    TrimCharacterInRemoteSpreadsheetRequest,
    UpdateWordCaseInRemoteSpreadsheetRequest,
)

from core import storage
from core.utils.spreadsheet_util import get_cells_cloud_client, resolve_worksheet_range


def _client():
    return get_cells_cloud_client()


def _execute(file_uuid, worksheet, _range, method, build_request) -> bool:
    """Resolve the target sheet/range once, then run a single mutation request.

    The file uuid is resolved through the registry first (raising a clear error
    for unknown/expired uuids) and the real cloud folder/name then drive both the
    structure read and the mutation. Worksheet/range semantics stay consistent
    (see ``resolve_worksheet_range``) and each call performs one structure read
    plus one edit instead of one edit per worksheet.
    """
    handle = storage.resolve(file_uuid)
    client = _client()
    raw = client.get_structure_in_remote_spreadsheet(
        GetStructureInRemoteSpreadsheetRequest(handle["name"], folder=handle["folder"]))
    structure = json.loads(raw)
    sheet_name, resolved_range = resolve_worksheet_range(structure, worksheet, _range)
    request = build_request(sheet_name, resolved_range, handle)
    response = getattr(client, method)(request)
    return response.status == "OK"


def trim_text(file_uuid, worksheet=None, _range=None, trim_text=' ') -> bool:
    def build(sheet, rng, handle):
        if trim_text == ' ':
            return TrimCharacterInRemoteSpreadsheetRequest(
                handle["name"], sheet, rng, trim_leading=True, trim_trailing=True, folder=handle["folder"])
        return TrimCharacterInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, trim_content=trim_text, trim_leading=True, trim_trailing=True, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "trim_character_in_remote_spreadsheet", build)


def trim_text_from_leading(file_uuid, worksheet=None, _range=None, trim_text=' ') -> bool:
    def build(sheet, rng, handle):
        if trim_text == ' ':
            return TrimCharacterInRemoteSpreadsheetRequest(
                handle["name"], sheet, rng, trim_leading=True, folder=handle["folder"])
        return TrimCharacterInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, trim_content=trim_text, trim_leading=True, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "trim_character_in_remote_spreadsheet", build)


def trim_text_from_trailing(file_uuid, worksheet=None, _range=None, trim_text=' ') -> bool:
    def build(sheet, rng, handle):
        if trim_text == ' ':
            return TrimCharacterInRemoteSpreadsheetRequest(
                handle["name"], sheet, rng, trim_trailing=True, folder=handle["folder"])
        return TrimCharacterInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, trim_content=trim_text, trim_trailing=True, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "trim_character_in_remote_spreadsheet", build)


def remove_extra_line_breaks(file_uuid, worksheet=None, _range=None) -> bool:
    def build(sheet, rng, handle):
        return TrimCharacterInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, remove_extra_line_breaks=True, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "trim_character_in_remote_spreadsheet", build)


def remove_all_line_breaks(file_uuid, worksheet=None, _range=None) -> bool:
    def build(sheet, rng, handle):
        return TrimCharacterInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, remove_all_line_breaks=True, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "trim_character_in_remote_spreadsheet", build)


def word_case(file_uuid, worksheet=None, _range=None, word_case_type='UpperCase') -> bool:
    def build(sheet, rng, handle):
        return UpdateWordCaseInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, word_case_type, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "update_word_case_in_remote_spreadsheet", build)


def _remove_character_set(file_uuid, worksheet, _range, character_sets) -> bool:
    def build(sheet, rng, handle):
        return RemoveCharactersInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, remove_text_method="RemoveCharacterSets",
            character_sets=character_sets, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "remove_characters_in_remote_spreadsheet", build)


def remove_non_printing_characters(file_uuid, worksheet=None, _range=None) -> bool:
    return _remove_character_set(file_uuid, worksheet, _range, "NonPrintingCharacters")


def remove_text_characters(file_uuid, worksheet=None, _range=None) -> bool:
    return _remove_character_set(file_uuid, worksheet, _range, "TextCharacters")


def remove_numeric_characters(file_uuid, worksheet=None, _range=None) -> bool:
    return _remove_character_set(file_uuid, worksheet, _range, "NumericCharacters")


def remove_symbols(file_uuid, worksheet=None, _range=None) -> bool:
    return _remove_character_set(file_uuid, worksheet, _range, "Symbols")


def remove_punctuation_marks(file_uuid, worksheet=None, _range=None) -> bool:
    return _remove_character_set(file_uuid, worksheet, _range, "PunctuationMarks")


def remove_custom_characters(file_uuid, worksheet=None, _range=None, custom_characters='', case_sensitive=False) -> bool:
    def build(sheet, rng, handle):
        return RemoveCharactersInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, remove_text_method="RemoveCustomCharacter",
            remove_custom_value=custom_characters, case_sensitive=case_sensitive, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "remove_characters_in_remote_spreadsheet", build)


def remove_first_n_characters(file_uuid, worksheet=None, _range=None, number=0) -> bool:
    def build(sheet, rng, handle):
        return RemoveCharactersByPositionInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, the_first_n_characters=number, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "remove_characters_in_remote_spreadsheet", build)


def remove_last_n_characters(file_uuid, worksheet=None, _range=None, number=0) -> bool:
    def build(sheet, rng, handle):
        return RemoveCharactersByPositionInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, the_last_n_characters=number, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "remove_characters_in_remote_spreadsheet", build)


def remove_before_text(file_uuid, worksheet=None, _range=None, text='', case_sensitive=False) -> bool:
    def build(sheet, rng, handle):
        return RemoveCharactersByPositionInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, all_characters_before_text=text,
            case_sensitive=case_sensitive, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "remove_characters_in_remote_spreadsheet", build)


def remove_after_text(file_uuid, worksheet=None, _range=None, text='', case_sensitive=False) -> bool:
    def build(sheet, rng, handle):
        return RemoveCharactersByPositionInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, all_characters_after_text=text,
            case_sensitive=case_sensitive, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "remove_characters_in_remote_spreadsheet", build)


def add_text_at_head(file_uuid, worksheet=None, _range=None, text='') -> bool:
    def build(sheet, rng, handle):
        return AddTextInRemoteSpreadsheetRequest(handle["name"], sheet, rng, text, "AtTheBeginning", folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "add_text_in_remote_spreadsheet", build)


def add_text_at_tail(file_uuid, worksheet=None, _range=None, text='') -> bool:
    def build(sheet, rng, handle):
        return AddTextInRemoteSpreadsheetRequest(handle["name"], sheet, rng, text, "AtTheEnd", folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "add_text_in_remote_spreadsheet", build)


def add_text_before_text(file_uuid, worksheet=None, _range=None, text='', select_text='') -> bool:
    def build(sheet, rng, handle):
        return AddTextInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, text, "BeforeText", select_text=select_text, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "add_text_in_remote_spreadsheet", build)


def add_text_after_text(file_uuid, worksheet=None, _range=None, text='', select_text='') -> bool:
    def build(sheet, rng, handle):
        return AddTextInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, text, "AfterText", select_text=select_text, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "add_text_in_remote_spreadsheet", build)


def convert_number_to_text(file_uuid, worksheet=None, _range=None) -> bool:
    def build(sheet, rng, handle):
        return ConvertTextInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, convert_text_type="ConvertNumberToText", folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "convert_text_in_remote_spreadsheet", build)


def convert_line_break_to_text(file_uuid, worksheet=None, _range=None, target_text='') -> bool:
    def build(sheet, rng, handle):
        return ConvertTextInRemoteSpreadsheetRequest(
            handle["name"], sheet, rng, convert_text_type="ConvertLinebreak",
            target_characters=target_text, folder=handle["folder"])
    return _execute(file_uuid, worksheet, _range, "convert_text_in_remote_spreadsheet", build)
