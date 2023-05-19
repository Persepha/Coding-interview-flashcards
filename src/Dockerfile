FROM python:3.10.4-slim

COPY .. /app
WORKDIR /app

RUN python3 -m  venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade &&  \
    /opt/venv/bin/pip install -r requirements.txt

RUN /opt/venv/uvicorn main:app --host 0.0.0.0 --port $PORT