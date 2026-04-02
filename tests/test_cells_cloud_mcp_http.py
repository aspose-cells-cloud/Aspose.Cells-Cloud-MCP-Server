import os

import pytest
import asyncio
import base64
import binascii
from fastmcp import Client

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

config = {
    "mcpServers": {
        "my-aspose-server": {
            "url": "http://127.0.0.1:8080/mcp",  # 你的服务端地址
            "transport": "streamable-http"
        }
    }
}


@pytest.mark.asyncio
class TestCellsCloudMCPHttp:

    async def test_full_workflow(self):

        async with Client(config) as client:
            # 2. Test by listing all available tools to verify that the service has started and is interactive
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]

            print(f"Available tools: {tool_names}")
            assert "convert_excel_to_pdf" in tool_names, "Expected 'convert_excel_to_pdf' tool to be registered."

            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")
            # print(book1_xlsx)
            result = await client.call_tool(
                name='convert_excel_to_pdf',
                arguments = {'spreadsheet_b64string': book1_xlsx}
            )
            if result.is_error:
                assert False
            else:
                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("Book1-Http.pdf", "wb") as file:
                    file.write(filedata)
                assert  True

            # # 4. Test abnormal situation
            # try:
            #     await client.call_tool(
            #         "convert_excel_to_pdf",
            #         {"file_name": "bad_file.csv", "output_name": "out.pdf"}
            #     )
            #     # If no exception is thrown above, the test fails
            #     assert False, "Expected a ValueError for invalid file format"
            # except Exception as e:
            #     # Caught the expected exception
            #     print(f"❌ Expected error caught: {e}")
            #     assert "Only support .xlsx" in str(e)
