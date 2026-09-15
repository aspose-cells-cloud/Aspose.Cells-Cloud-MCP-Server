import base64
import json
import os
from pathlib import Path
from asposecellscloud.models import SaveOptionsData
from asposecellscloud.requests import (
    ConvertSpreadsheetRequest,
    ConvertSpreadsheetToCsvRequest,
    ConvertSpreadsheetToJsonRequest,
    ConvertSpreadsheetToPdfRequest,
    SaveSpreadsheetAsRequest,
)

from core import storage
from core.formats import apply_fit_mode, get_save_options_with_save_format
from core.utils.spreadsheet_util import get_cells_cloud_client


def _read_and_remove(temp_file_path: str) -> str:
    """Read a temporary file returned by the SDK, delete it, return Base64 text."""
    try:
        with open(temp_file_path, "rb") as file:
            file_bytes = file.read()
        return base64.b64encode(file_bytes).decode('utf-8')
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def _save_as(file_uuid: str, target_format: str, save_options_data: SaveOptionsData) -> str | None:
    """Run one cloud save-as and register the produced file in the registry.

    The output uuid is :func:`storage.allocate`d first so its cloud path can be
    told to the API via ``save_options_data.filename``; the reservation is
    committed only when the cloud reports success and aborted (never left
    dangling) on failure. The source workbook is resolved through the registry so
    its real cloud folder/name drive the request.
    """
    source = storage.resolve(file_uuid)
    # The output is named after the source with the target extension, so a
    # downloaded artifact keeps a meaningful name (book1.pdf rather than File).
    # original_name is None for an upload made without file_name, so fall back to
    # the handle's cloud object name (the default "File") — that value is always
    # present, keeping the output name well-defined for unnamed uploads too.
    original_name = source.get("original_name")
    new_name = str(Path(original_name or source["name"]).with_suffix(f".{target_format}"))
    output_uuid = storage.allocate(original_name=original_name, source="converted", name=new_name)
    # The /saveas endpoint is given a root-relative storage path ("<out_uuid>/<name>")
    # so the output lands where download_file resolves it. This is covered by the
    # live Docker test (tests/test_cells_cloud_mcp_docker.py::
    # test_upload_save_download_workflow), which saves as and then downloads the
    # result; the registry path layout is derived in core/storage.path_for.
    save_options_data.filename = storage.path_for(output_uuid, new_name)
    request = SaveSpreadsheetAsRequest(
        source["name"], target_format,
        save_options_data=save_options_data, folder=source["folder"])
    try:
        response = get_cells_cloud_client().save_spreadsheet_as(request)
    except Exception:
        storage.abort(output_uuid)
        raise
    if "OK" == response.status:
        storage.commit(output_uuid)
        return output_uuid
    storage.abort(output_uuid)
    # Surface a failed cloud save as an error instead of a silent None, so an
    # agent never receives a bare "None" file_token for a write that did not happen.
    raise RuntimeError(
        f"Save-as to {target_format!r} failed with cloud status: {response.status!r}")


def save_spreadsheet_as(file_uuid: str, target_format: str) -> str:
    save_options_data = SaveOptionsData()
    return _save_as(file_uuid, target_format, save_options_data)


def save_spreadsheet_as_with_scaling_mode(file_uuid: str, target_format: str, scaling_mode: str) -> str:
    save_options_data = SaveOptionsData()
    mode = (scaling_mode or "").strip()
    if mode and mode.lower() != "noscaling":
        save_options = get_save_options_with_save_format(target_format)
        if save_options is None:
            raise ValueError(
                f"scaling_mode cannot be applied: no typed save options exist for target format {target_format!r}."
            )
        apply_fit_mode(save_options, mode)  # raises ValueError for unsupported modes/formats
        save_options_data.save_options = save_options
    return _save_as(file_uuid, target_format, save_options_data)


def save_spreadsheet_as_with_save_options_json_data(file_uuid: str, target_format: str, save_options_json_data: str) -> str:
    save_options_data = SaveOptionsData()
    save_options = get_save_options_with_save_format(target_format)
    if save_options_json_data and save_options is not None:
        _apply_json_save_options(save_options, save_options_json_data)
        save_options_data.save_options = save_options
    return _save_as(file_uuid, target_format, save_options_data)


def _declared_fields(save_options) -> set[str]:
    """Attribute names a save-options model declares (its own + inherited fields).

    The Aspose SDK models carry an ``attribute_map`` (snake_case attribute ->
    public/PascalCase API name) on every class in the hierarchy, so the declared
    set is the union across the MRO. Models without such metadata return an empty
    set (the caller then falls back to ``hasattr``).
    """
    declared = set()
    for klass in type(save_options).__mro__:
        attribute_map = getattr(klass, "attribute_map", None)
        if isinstance(attribute_map, dict):
            declared.update(attribute_map)
    return declared


def _apply_json_save_options(save_options, save_options_json_data: str) -> None:
    """Apply user-provided JSON options onto a typed save-options model in place.

    Keys may be the model's snake_case attribute names (``display_doc_title``) or
    its public/PascalCase API field names (``DisplayDocTitle``); both route to the
    same attribute. Keys the selected options model does not declare raise a
    ``ValueError`` instead of being silently dropped, and malformed or non-object
    JSON is rejected with a clear message — matching the fail-loud policy used for
    scaling modes (see core.formats.apply_fit_mode).
    """
    if not save_options_json_data:
        return
    try:
        data = json.loads(save_options_json_data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"save_options_json_data is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("save_options_json_data must be a JSON object of option names and values.")

    declared = _declared_fields(save_options)
    # Reverse the attribute_map so PascalCase API names resolve to attributes too.
    api_name_to_field = {
        api_name: field
        for klass in type(save_options).__mro__
        for field, api_name in (getattr(klass, "attribute_map", None) or {}).items()
    }

    resolved = {}
    for key, value in data.items():
        field = key if (not declared or key in declared) else api_name_to_field.get(key)
        if not declared:
            # No field metadata: fall back to touching existing attributes only.
            if not hasattr(save_options, field):
                raise ValueError(f"Unknown save option {key!r} for {type(save_options).__name__}.")
        if field is None:
            raise ValueError(
                f"Unknown save option {key!r} for {type(save_options).__name__}. "
                f"Supported options: {sorted(declared)}."
            )
        resolved[field] = value

    for field, value in resolved.items():
        setattr(save_options, field, value)


def convert_spreadsheet_to_pdf(spreadsheet_b64string: str) -> str:
    request = ConvertSpreadsheetToPdfRequest(base64.b64decode(spreadsheet_b64string.strip()))
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_pdf(request)
    return _read_and_remove(temp_file_path)


def convert_excel_to_csv(spreadsheet_b64string: str) -> str:
    request = ConvertSpreadsheetToCsvRequest(base64.b64decode(spreadsheet_b64string.strip()))
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_csv(request)
    return _read_and_remove(temp_file_path)


def convert_spreadsheet_to_json(spreadsheet_b64string: str) -> str:
    request = ConvertSpreadsheetToJsonRequest(base64.b64decode(spreadsheet_b64string.strip()))
    temp_file_path = get_cells_cloud_client().convert_spreadsheet_to_json(request)
    return _read_and_remove(temp_file_path)


def convert_spreadsheet(spreadsheet_b64string: str, format: str) -> str:
    request = ConvertSpreadsheetRequest(base64.b64decode(spreadsheet_b64string.strip()), format=format)
    temp_file_path = get_cells_cloud_client().convert_spreadsheet(request)
    return _read_and_remove(temp_file_path)
