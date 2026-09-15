# Windows (Server Core) image used for deployments that must run offline.
#
# NOTE: building it requires a populated ./packages/ directory (a python
# installer and the pinned wheels for pip --no-index) that is gitignored and
# produced by the release pipeline. For a general-purpose Linux image use
# Dockerfile.Linux instead.
#
# Provide Aspose Cloud credentials at run time via ASPOSE_CLOUD_CLIENT_ID /
# ASPOSE_CLOUD_CLIENT_SECRET and select a transport with MCP_TRANSPORT
# (stdio | streamable-http | sse).

FROM mcr.microsoft.com/windows/servercore:ltsc2019
WORKDIR  C:/app
COPY packages C:\\app\\packages
COPY requirements.txt .
RUN C:\\app\\packages\\python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\\Python
RUN C:\Python\python.exe -m pip install --no-index --find-links=C:\\app\\packages --no-cache-dir -r requirements.txt
COPY mcp_server.py .
COPY core ./core
# Registry maintenance helper (scripts/init_registry_db.py), for pre-creating or
# migrating registry.db on a freshly mounted volume.
COPY scripts ./scripts
COPY LICENSE   .
ENV PYTHONDONTWRITEBYTECODE=1
# FastMCP checks PyPI at startup to print a "new version available" banner. That
# outbound call is pointless in a production container and delays or fails on a
# cluster without egress to PyPI. Values are "stable" | "prerelease" | "off".
ENV FASTMCP_CHECK_FOR_UPDATES=off
EXPOSE 8080
CMD ["C:\\Python\\python.exe", "mcp_server.py"]
