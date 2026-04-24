![](https://img.shields.io/badge/aspose.cells%20Cloud%20MCP-26.4.0-green?style=for-the-badge&logo=python)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

**Aspose.Cells Cloud MCP Server** is a FastMCP-based MCP server built on top of [Aspose.Cells Cloud SDK for Python](https://products.aspose.cloud/cells/python/). It automates the creation and editing of Microsoft Excel spreadsheets and exposes operations as MCP tools that any MCP-compatible client can call. Supported transports: `stdio`, `streamable-http`, `sse`.

## Features

- convert spreadsheet

## Requirements

- Python 3.11+
- [Aspose.Cells Cloud SDK for Python](https://products.aspose.cloud/cells/python/). This library is a [commercial product](https://purchase.aspose.cloud/buy/cells/python).  
  You'll need to obtain a valid license for Aspose.Cells Cloud. The package will install this dependency, but you're responsible for complying with Aspose's licensing terms.

## Installation

```powershell

python -m pip install aspose-cells-cloud-mcp

```

From source (download repo and install requirements):

```powershell

git clone https://github.com/aspose-cells-cloud/Aspose.Cells-Cloud-MCP-Server
cd Aspose.Cells-Cloud-MCP-Server
python -m pip install -r requirements.txt

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

## How to run Aspose Cells Cloud MCP Server in Docker Container

### Build Docker Image

```cmd

docker build -t aspose-cells-cloud-mcp-server:26.4.0 .

```

### Run Docker Image

```cmd

 docker run -itdp 28080:8080  -e MCP_TRANSPORT="streamable-http" -e ASPOSE_CLOUD_CLIENT_ID="yourt-aspose-cloud-client_id" -e ASPOSE_CLOUD_CLIENT_SECRET="your-aspose-cloud-client-secret" --isolation hyperv  --name my-aspose-cells-cloud-mcp-instance  aspose-cells-cloud-mcp-server:26.4.0

```

## License

This package is licensed under the MIT License. However, it depends on Aspose.Cells Cloud SDK for Python library, which is an open-source library.

You must obtain valid client credentials for Aspose.Cells Cloud.

## Aspose.Cells Cloud License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

The Aspose.Cells Cloud API itself requires a separate subscription a free tier is available at [aspose.cloud](https://purchase.aspose.cloud/pricing).

## Integration with MCP Clients

- Claude Desktop MCP: add this server with `streamable-http` or `sse` transport and the URL printed by the server at startup.
- Any MCP (JSON) clients — configure the matching transport and path.
