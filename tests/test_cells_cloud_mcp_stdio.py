import os

import pytest
import asyncio
import base64
import binascii
from fastmcp import Client
from fastmcp.client import StdioTransport

from tests.test_data_handler import get_book_text_ods, get_book1_xlsx, get_booktext_xlsx

SERVER_FILE_PATH = "mcp_server.py"


@pytest.mark.asyncio
class TestCellsCloudMCPStdio:

    async def test_full_workflow(self):
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
            # 2. Test by listing all available tools to verify that the service has started and is interactive
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]

            print(f"Available tools: {tool_names}")
            assert "convert_spreadsheet" in tool_names, "Expected 'convert_spreadsheet' tool to be registered."

            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='convert_spreadsheet',
                arguments = {'spreadsheet_b64string': book1_xlsx,'format':'pdf'}
            )

            if result.is_error:
                assert False
            else:

                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                filedata = base64.b64decode(success_message)
                with open("convert_spreadsheet.pdf", "wb") as file:
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
    async def test_convert_excel_to_csv_workflow(self):
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
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
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
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
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
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
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
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
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
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
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
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
    async def test_get_excel_structure_workflow(self):
        """
        Test the complete stdio workflow: connect -> initialize -> list tools -> call tools
        The Client of FastMCP automatically handles stdio communication.
        """
        # 1. Start the client, it will automatically start the server.py subprocess
        # Note: Here, a file path is passed, not a module instance
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
            # 3. Use the tool for normal testing
            book1_xlsx = get_book1_xlsx()
            if book1_xlsx is None or len(book1_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='get_spreadsheet_structure',
                arguments={'spreadsheet_b64string': book1_xlsx}
            )

            if result.is_error:
                assert False
            else:
                success_message = "".join([c.text for c in result.content if hasattr(c, 'text')])
                print(success_message)
                # with open("test_get_excel_structure_workflow.json", "wb") as file:
                #     file.write(success_message)
                assert True

    async def test_edit_workflow(self):
        env_vars = {"ASPOSE_CLOUD_API_URL": os.getenv("CellsCloudTestApiBaseUrl"),"ASPOSE_CLOUD_CLIENT_ID": os.getenv("CellsCloudTestClientId"),"ASPOSE_CLOUD_CLIENT_SECRET": os.getenv("CellsCloudTestClientSecret")}
        transport = StdioTransport(
            command="python",
            args=[SERVER_FILE_PATH],
            env=env_vars
        )
        async with Client(transport) as client:
            # 3. Use the tool for normal testing
            book_text_xlsx = get_booktext_xlsx()
            if book_text_xlsx is None or len(book_text_xlsx) == 0:
                print("Do not get book1.xlsx")

            result = await client.call_tool(
                name='upload_file',
                arguments={'file_content_b64string': book_text_xlsx}
            )

            if result.is_error:
                assert False

            file_token =  "".join([c.text for c in result.content if hasattr(c, 'text')])

            result = await client.call_tool(
                name='trim_text_from_trailing',
                arguments={'file_token': file_token,"worksheet":"Text","_range":"D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='trim_text_from_leading',
                arguments={'file_token': file_token,"worksheet":"Text","_range":"D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_extra_line_breaks',
                arguments={'file_token': file_token,"worksheet":"Text","_range":"D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_all_line_breaks',
                arguments={'file_token': file_token,"worksheet":"Text","_range":"D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='word_case',
                arguments={'file_token': file_token, "worksheet": "Text", "_range": "D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_non_printing_characters',
                arguments={'file_token': file_token}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_text_characters',
                arguments={'file_token': file_token}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_numeric_characters',
                arguments={'file_token': file_token}
            )

            if result.is_error:
                assert False
            result = await client.call_tool(
                name='remove_symbols',
                arguments={'file_token': file_token}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_punctuation_marks',
                arguments={'file_token': file_token}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='upload_file',
                arguments={'file_content_b64string': book_text_xlsx}
            )

            if result.is_error:
                assert False

            file_token =  "".join([c.text for c in result.content if hasattr(c, 'text')])

            result = await client.call_tool(
                name='remove_custom_characters',
                arguments={'file_token': file_token, 'custom_characters':'\t'}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_first_n_characters',
                arguments={'file_token': file_token,"number":2,"worksheet":"Text","_range":"D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_last_n_characters',
                arguments={'file_token': file_token,"number":2,"worksheet":"Text","_range":"D4:D4"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_before_text',
                arguments={'file_token': file_token, "text": "Aspose"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='remove_after_text',
                arguments={'file_token': file_token, "text": "Aspose"}
            )

            if result.is_error:
                assert False
            result = await client.call_tool(
                name='add_text_at_head',
                arguments={'file_token': file_token, "text": "Aspose"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='add_text_at_tail',
                arguments={'file_token': file_token, "text": "Cells"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='add_text_before_text',
                arguments={'file_token': file_token, "text": "Cells","select_text":"Aspose."}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='add_text_after_text',
                arguments={'file_token': file_token, "text": " Cloud","select_text":"Aspose.Cells"}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='convert_number_to_text',
                arguments={'file_token': file_token}
            )

            if result.is_error:
                assert False

            result = await client.call_tool(
                name='convert_line_break_to_text',
                arguments={'file_token': file_token,"target_text":"\t"}
            )

            if result.is_error:
                assert False