# Aspose.Cells Cloud MCP Server

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview
**Aspose.Cells Cloud MCP Server** is a FastMCP-based MCP server built on top of [Aspose.Cells Cloud SDK for Python](https://products.aspose.cloud/cells/python/). It automates Microsoft Excel spreadsheet creation and editing and exposes operations as MCP tools that any MCP-compatible client can call. Supported transports: `stdio`, `streamable-http`, `sse`.

## Features

- Upload the spreadsheet to Aspose Cloud Storage.
- Save the spreadsheet as different format file in Aspose Cloud Storage.
- 

## Requirements

- Python 3.11+
- [Aspose.Cells Cloud SDK for Python](https://products.aspose.cloud/cells/python/). This library is a [commercial product](https://purchase.aspose.cloud/buy/cells/python).  
You'll need to obtain a valid license for Aspose.Cells Cloud. The package will install this dependency, but you're responsible for complying with Aspose's licensing terms.

## Installation

```bash
pip install aspose-cells-cloud-mcp
```

From source (download repo and install requirements):

```bash
git clone https://github.com/aspose-cells-cloud/Aspose.Cells-Cloud-MCP-Server
cd Aspose.Cells-Cloud-MCP-Server
pip install -r requirements.txt
```

## Command Line Interface

After installation, the CLI command is available:

```bash
aspose-cells-cloud-mcp
```

By default, the server runs with the `stdio` transport.

Run without installation:

```bash
python mcp_server.py
```

## Transports and Configuration

Supported MCP transports: `stdio`, `streamable-http`, `sse`.

### Environment Variables

- `MCP_TRANSPORT` — `stdio` | `streamable-http` | `sse` (default `stdio`)
- `MCP_HOST` — host address (default `0.0.0.0`)
- `MCP_PORT` — port (default `8080`)
- `MCP_PATH` — HTTP path for `streamable-http` (default `/mcp`)
- `MCP_SSE_PATH` — events path for `sse` (default `/sse`)
- `LOG_LEVEL` — logging level (`INFO`, `DEBUG`, ...)


## Aspose.Cells Cloud License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

The Aspose.HTML Cloud API itself requires a separate subscription � a free tier is available at [aspose.cloud](https://purchase.aspose.cloud/pricing).

## Tools

See full list and signatures in `mcp_server.py` (function `register_tools`) and tests in `tests/features/*`.

Main tool categories:

- content/reading: create document, insert/delete/read text, headings, lists, HTML/Markdown
- layout: pages, breaks, columns, headers/footers, page numbering
- tables: create and format tables
- watermarks: watermarks
- links/bookmarks: hyperlinks and bookmarks
- properties: document properties
- protection: protection and restrictions
- comments/notes: comments, footnotes/endnotes
- export/render: export, page rendering

## Example Workflow via an MCP Client

Sequence of tool calls (names match the server):

1. `create_document` → get `doc_id`
2. `add_heading` (e.g., levels 1–3)
3. `add_paragraph` / `insert_text_end`
4. `add_table_end` or `add_table_at_paragraph`
5. `add_watermark_text` or `add_watermark_image_base64`
6. `export_base64` (e.g., `fmt="pdf"`) — get file as Base64

## Integration with MCP Clients

- Claude Desktop MCP: add this server with `streamable-http` or `sse` transport and the URL printed by the server at startup.
- Any MCP (JSON) clients — configure the matching transport and path.

## License

This package is licensed under the MIT License. However, it depends on Aspose.Words for Python via .Net library, which is proprietary, closed-source library.

⚠️ You must obtain valid license for Aspose.Words for Python via .Net library. This repository does not include or distribute any proprietary components.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Use of third-party trademarks or logos is subject to those third-party policies.