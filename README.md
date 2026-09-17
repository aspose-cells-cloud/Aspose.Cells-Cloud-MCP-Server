# Aspose.Cells Cloud MCP Server

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

**Aspose.Cells Cloud MCP Server** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
server built with [FastMCP](https://github.com/jlowin/fastmcp) on top of the
[Aspose.Cells Cloud SDK for Python](https://products.aspose.cloud/cells/python/).
It exposes spreadsheet automation — file conversion, structure inspection, text
cleaning/editing — as MCP tools that any MCP-compatible client (Claude Desktop,
Cline, custom agents, …) can call.

```
https://api.aspose.cloud/cells/mcp
```

## Features

- Upload / download workbooks to Aspose Cloud Storage (Base64 <-> `file_uuid`).
- Inspect the full structure of a workbook as JSON (metadata, worksheets, tables
  with column formulas, pivot tables, charts, shape coordinates).
- Convert workbooks to PDF, CSV, JSON, HTML, XPS, ODS, images, … — either from
  cloud storage or directly from a Base64 payload.
- Save-as with print-scaling modes and/or arbitrary JSON save options.
- Clean & edit cell text in place: trim, remove characters by type/position/pattern,
  add text, fix line breaks, change word case, convert numbers to text.

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

```powershell
python .\mcp_server.py
```

## Transports and Configuration

The transport is chosen with `MCP_TRANSPORT` (`stdio` | `streamable-http` | `sse`),
falling back to the `TRANSPORT` variable and then `stdio`. HTTP transports listen
for MCP clients; the same process also serves two plain HTTP endpoints,
`/health` and `/version`.

| Environment variable | Default            | Meaning                                  |
| -------------------- | ------------------ | ---------------------------------------- |
| `MCP_TRANSPORT`      | `stdio`            | Transport: `stdio`, `streamable-http`, `sse` |
| `MCP_HOST`           | `0.0.0.0`          | Bind address for HTTP transports         |
| `MCP_PORT`           | `8080`             | Port for HTTP transports                 |
| `MCP_PATH`           | `/mcp`             | Path for `streamable-http`               |
| `MCP_SSE_PATH`       | `/sse`             | Events path for `sse`                    |
| `LOG_LEVEL`          | `INFO`             | Logging verbosity                         |
| `MCP_STATE_DIR`      | *(platform data dir)* | Directory for the local state DB (`registry.db`). Set this to a writable volume in containers. |
| `MCP_FILE_TTL_HOURS` | *(unset → never)* | Optional hours-after-*registration* (not last use) before a stored `file_uuid` stops resolving. Expires the local handle only — it does not delete the cloud file (see below). |
| `MCP_CLOUD_TIMEOUT_SECONDS` | `300`          | Upper bound (seconds) for each Aspose Cloud HTTP call made by the SDK. The SDK otherwise sets no timeout, so a stalled or unreachable backend would hang a tool forever; set `0` to disable the bound. |

## How to run Aspose Cells Cloud MCP Server in Docker Container

### Build Docker Image

```cmd

docker build -t aspose-cells-cloud-mcp-server:26.4.0 .

```

### Run Docker Image

```cmd

 docker run -itdp 28080:8080  -e MCP_TRANSPORT="streamable-http" -e ASPOSE_CLOUD_CLIENT_ID="yourt-aspose-cloud-client_id" -e ASPOSE_CLOUD_CLIENT_SECRET="your-aspose-cloud-client-secret" -e MCP_STATE_DIR="C:\state" --isolation hyperv  --name my-aspose-cells-cloud-mcp-instance  aspose-cells-cloud-mcp-server:26.9.0

```

## Aspose.Cells Cloud License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

The Aspose.Cells Cloud API itself requires a separate subscription � a free tier is available at [aspose.cloud](https://purchase.aspose.cloud/pricing).

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Use of third-party trademarks or logos is subject to those third-party policies.