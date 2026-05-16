import os

from asposecellscloud import CellsApi

def apply_license(client_id:str, client_secret:str):
    os.environ["ASPOSE_CLOUD_CLIENT_ID"] = client_id
    os.environ["ASPOSE_CLOUD_CLIENT_SECRET"] =client_secret
    cells_cloud_client = get_cells_cloud_client()

def get_cells_cloud_client()->CellsApi:
    base_url = os.getenv("ASPOSE_CLOUD_API_URL")
    if base_url is None or len(base_url.strip()) ==0:
        return CellsApi(os.getenv("ASPOSE_CLOUD_CLIENT_ID"), os.getenv("ASPOSE_CLOUD_CLIENT_SECRET"))
    else:
        return CellsApi(os.getenv("ASPOSE_CLOUD_CLIENT_ID"), os.getenv("ASPOSE_CLOUD_CLIENT_SECRET"),
                        base_uri=os.getenv("ASPOSE_CLOUD_API_URL"))
    
def num_to_cell(row, col):
    col += 1
    column_name = ""
    while col > 0:
        col -= 1
        column_name = chr(col % 26 + 65) + column_name
        col //= 26  
    return f"{column_name}{row + 1}"