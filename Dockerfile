
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app.py /app
COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt
RUN pip install prometheus_client
