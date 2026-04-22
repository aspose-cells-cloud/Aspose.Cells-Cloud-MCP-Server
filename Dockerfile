FROM mcr.microsoft.com/windows/servercore:ltsc2019
#FROM python:3.12-windowsservercore
WORKDIR  C:/app
COPY packages C:\\app\\packages
COPY requirements.txt .
RUN C:\\app\\packages\\python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\\Python
#RUN C:\Python\python.exe -m pip install --no-index --find-links=C:\\app\\packages --no-deps --force-reinstall -r requirements.txt
RUN C:\Python\python.exe -m pip install --no-index --find-links=C:\\app\\packages --no-cache-dir -r requirements.txt
COPY mcp_server.py .
COPY core ./core
COPY LICENSE   .
RUN dir /s /b
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["C:\\Python\\python.exe", "mcp_server.py"]
#
#FROM mcr.microsoft.com/windows/servercore:ltsc2022
#FROM mcr.microsoft.com/windows/servercore:ltsc2022
#ENV PYTHON_VERSION=3.12.0
#ENV PYTHON_PATH=C:\\Python
#ENV PATH=%PYTHON_PATH%;%PYTHON_PATH%\\Scripts;%PATH%
#
#ADD https://aka.ms/vs/17/release/vc_redist.x64.exe C:\\vc_redist.x64.exe
#RUN C:\\vc_redist.x64.exe /quiet /install
#
#ADD https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe C:\\python-installer.exe
#RUN C:\\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\\Python
#
#WORKDIR C:\\app
#COPY packages C:\\app\\packages
#COPY requirements.txt .
#
##RUN python -m pip install --no-cache-dir -r requirements.txt
#RUN  C:\\Python\\python.exe -m pip install --no-index --find-links=C:\\app\\packages -r requirements.txt
#COPY mcp_server.py .
#COPY core\     .
#COPY LICENSE   .
#
#EXPOSE 8000
#
#CMD ["C:\\Python\\python.exe", "server.py"]