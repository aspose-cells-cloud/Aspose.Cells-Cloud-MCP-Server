import base64
import os

from asposecellscloud import DownloadFileRequest, UploadFileRequest

from core import storage
from core.utils.spreadsheet_util import get_cells_cloud_client


def upload_file(file_content_b64string: str, file_name: str | None = None) -> str:
    """Upload raw file bytes (Base64 text) to Aspose Cloud Storage; returns a file uuid.

    The upload request targets the uuid *folder* (:func:`storage.upload_folder`)
    with a part named after ``file_name``, so the file is stored **as its own
    name** directly under the uuid folder: ``<uuid>/report.xlsx`` for an upload
    named ``report.xlsx``, and ``<uuid>/File`` when ``file_name`` is empty — the
    exact location every consumer resolves from the handle. The folder being the
    unique uuid means two uploads sharing a file name never collide.
    """
    object_name = storage.object_name(file_name)
    original_name = os.path.basename(file_name.strip()) if file_name and file_name.strip() else None
    file_uuid = storage.create(original_name=original_name, name=object_name, source="uploaded")
    request = UploadFileRequest(
        {object_name: base64.b64decode(file_content_b64string.strip())},
        storage.upload_folder(file_uuid))
    try:
        get_cells_cloud_client().upload_file(request)
    except Exception:
        storage.remove(file_uuid)  # don't leave a dangling handle for a failed upload
        raise
    return file_uuid


def download_file(file_uuid: str) -> str:
    """Download the file identified by ``file_uuid``; returns its content as Base64 text."""
    handle = storage.resolve(file_uuid)  # validate / refresh last-use before downloading
    request = DownloadFileRequest(storage.path_for(handle["folder"], handle["name"]))
    temp_path = get_cells_cloud_client().download_file(request)
    try:
        with open(temp_path, 'rb') as file:
            file_content = file.read()
        return base64.b64encode(file_content).decode('utf-8')
    finally:
        # Guard against removing a file the client never produced, so a failure to
        # open/read it is not masked by a FileNotFoundError raised in cleanup.
        if os.path.exists(temp_path):
            os.remove(temp_path)
