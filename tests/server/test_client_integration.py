import asyncio
import base64
import os
from contextlib import asynccontextmanager

from fastmcp import Client


@asynccontextmanager
async def _client_session(mcp_client_config):
    client = Client(mcp_client_config)
    async with client:
        yield client


def test_client_upload_spreadsheet(mcp_client_config, file_path):
    async def run_client():
        async with _client_session(mcp_client_config) as client:
            doc_id = await _create_document_and_get_id(client)
            await client.call_tool(name='add_paragraph', arguments={'doc_id': doc_id, 'text': 'Created document: OK'})
            await _save_exported_to_file(result_file_path, client, doc_id)

    _run_and_assert_file(result_file_path, run_client)