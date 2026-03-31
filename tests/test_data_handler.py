import base64

def get_book1_xlsx()->str:
    try:
        with open("D:\\cells.cloud-4.0\\src\\testdata\\Book1.xlsx", "rb") as f:
            binary_data = f.read()
            base64_bytes = base64.b64encode(binary_data)
            base64_str = base64_bytes.decode('utf-8')
            return base64_str
    except Exception as e:
        print(e)
        return ""