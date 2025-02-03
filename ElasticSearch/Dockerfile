FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
COPY ElasticSearch.py /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ElasticSearch.py"]