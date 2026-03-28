import os

from asposecellscloud import CellsApi

def apply_license(client_id:str, client_secret:str):
    os.environ["ASPOSE_CLOUD_CLIENT_ID"] = client_id
    os.environ["ASPOSE_CLOUD_SECRET_KEY"] =client_secret
    cells_cloud_client = get_cells_cloud_client()

def get_cells_cloud_client()->CellsApi:
    return CellsApi( os.getenv("ASPOSE_CLOUD_CLIENT_ID"), os.getenv("ASPOSE_CLOUD_CLIENT_SECRET"))
