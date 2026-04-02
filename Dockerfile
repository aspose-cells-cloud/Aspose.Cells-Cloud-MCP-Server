FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY server.py .
COPY aliases\  .
COPY core\     .
COPY LICENSE   .


EXPOSE 8000

CMD ["python", "server.py"]