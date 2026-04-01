import os

import pytest
import asyncio
import base64
import binascii
from fastmcp import Client
from fastmcp.client import StdioTransport

from tests.test_data_handler import get_book1_xlsx

SERVER_FILE_PATH = "mcp_server.py"



def is_valid_base64(s):
    if not isinstance(s, str):
        return False

    try:
        decoded = base64.b64decode(s, validate=True)
        re_encoded = base64.b64encode(decoded).decode('utf-8')
        return re_encoded == s
    except (binascii.Error, ValueError):
        return False


@pytest.mark.asyncio
class TestCellsCloudMCPStdio:

    async def test_full_workflow(self):
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
            # os.environ["ASPOSE_CLOUD_CLIENT_ID"] = "a73d6131-1f51-4fde-bc2e-bd499ed3fc22"
            # os.environ["ASPOSE_CLOUD_CLIENT_SECRET"] = "b770daf30685a37aa61c08ddcbf232b2"
            # 2. Test by listing all available tools to verify that the service has started and is interactive
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]

            print(f"Available tools: {tool_names}")
            assert "convert_local_excel_to_pdf" in tool_names, "Expected 'convert_local_excel_to_pdf' tool to be registered."

            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")
            # print(book1_xlsx)
            result = await client.call_tool(
                name='convert_local_excel_to_pdf',
                arguments = {'excel_b64string': book1_xlsx}
            )
            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("Book1.pdf", "wb") as file:
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
