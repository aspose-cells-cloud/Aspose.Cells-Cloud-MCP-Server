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
# migrating registry.db on a freshly mounted volume. Also used below to bake a
# ready registry.db into the image.
COPY scripts ./scripts
COPY LICENSE   .
ENV PYTHONDONTWRITEBYTECODE=1
# Where registry.db lives. Set explicitly so the image is self-contained: left
# unset, the server falls back to the platform user-data directory
# (platformdirs), whose location inside a Windows container is not predictable.
# Mount a volume on this path in production to keep file_uuid handles valid
# across pod recreation — the mount shadows the baked file below, which is
# harmless, since core.storage.init() recreates or migrates the schema on first
# use either way.
ENV MCP_STATE_DIR=C:\\state
# Bake a ready registry.db (schema + indexes, no rows) into the image so a bare
# `docker run` with no volume works out of the box. The schema comes from
# core.storage via the script, so it cannot drift from what the runtime expects;
# init() is idempotent, so a later schema change is applied on first start rather
# than breaking on the pre-existing file.
RUN C:\\Python\\python.exe scripts\\init_registry_db.py
# FastMCP checks PyPI at startup to print a "new version available" banner. That
# outbound call is pointless in a production container and delays or fails on a
# cluster without egress to PyPI. Values are "stable" | "prerelease" | "off".
ENV FASTMCP_CHECK_FOR_UPDATES=off
EXPOSE 8080
CMD ["C:\\Python\\python.exe", "mcp_server.py"]
