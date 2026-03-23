import os

from asposecellscloud import CellsApi


def get_cells_cloud_client()->CellsApi:
    return CellsApi( os.getenv("CELLS_CLOUD_CLIENT_ID"), os.getenv("CELLS_CLOUD_CLIENT_SECRET"))