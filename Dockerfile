FROM mcr.microsoft.com/windows/servercore:ltsc2019
WORKDIR  C:/app
COPY packages C:\\app\\packages
COPY requirements.txt .
RUN C:\\app\\packages\\python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\\Python
RUN C:\Python\python.exe -m pip install --no-index --find-links=C:\\app\\packages --no-cache-dir -r requirements.txt
COPY mcp_server.py .
COPY core ./core
COPY LICENSE   .
RUN dir /s /b
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["C:\\Python\\python.exe", "mcp_server.py"]
