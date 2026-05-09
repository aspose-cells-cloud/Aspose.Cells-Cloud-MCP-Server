import os

import pytest
import asyncio
import base64
import binascii
from fastmcp import Client

from tests.test_data_handler import get_book_text_ods, get_book1_xlsx

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


    async def test_convert_excel_to_csv_workflow(self):
        async with Client(config) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='convert_excel_to_csv',
                arguments = {'spreadsheet_b64string': book1_xlsx}
            )

            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("test_convert_excel_to_csv_workflow.csv", "wb") as file:
                    file.write(filedata)
                assert  True
    async def test_convert_excel_to_pdf_workflow(self):
        async with Client(config) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='convert_excel_to_pdf',
                arguments = {'spreadsheet_b64string': book1_xlsx}
            )

            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("test_convert_excel_to_pdf_workflow.pdf", "wb") as file:
                    file.write(filedata)
                assert  True
    async def test_convert_ods_to_pdf_workflow(self):
        async with Client(config) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book_text_ods()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='convert_ods_to_pdf',
                arguments = {'ods_b64string': book1_xlsx}
            )

            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("test_convert_ods_to_pdf_workflow.pdf", "wb") as file:
                    file.write(filedata)
                assert  True
    async def test_convert_excel_to_json_workflow(self):
        async with Client(config) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='convert_excel_to_json',
                arguments={'spreadsheet_b64string': book1_xlsx}
            )

            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("test_convert_excel_to_json_workflow.json", "wb") as file:
                    file.write(filedata)
                assert True

    async def test_convert_excel_workflow(self):
        async with Client(config) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='convert_spreadsheet',
                arguments={'spreadsheet_b64string': book1_xlsx,'format':'pdf'}
            )

            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("test_convert_excel_workflow.pdf", "wb") as file:
                    file.write(filedata)
                assert True
    async def test_upload_save_download_workflow(self):
        async with Client(config) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='upload_file',
                arguments={'file_content_b64string': book1_xlsx}
            )

            if result.is_error:
                assert False

            file_token =  "".join([c.text for c in result.content if hasattr(c, 'text')])

            result = await client.call_tool(
                name='save_spreadsheet_as',
                arguments={'file_token': file_token,"target_format":"pdf"}
            )

            if result.is_error:
                assert False

            file_token = "".join([c.text for c in result.content if hasattr(c, 'text')])

            result = await client.call_tool(
                name='download_file',
                arguments={'file_token': file_token}
            )
            if result.is_error:
                assert False
            else:
                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("book1_xlsx_download.xlsx", "wb") as file:
                    file.write(filedata)
                assert True