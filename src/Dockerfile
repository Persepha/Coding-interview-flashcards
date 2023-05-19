FROM python:3.10.4-slim

COPY .. /app
WORKDIR /app

RUN pip install pip --upgrade &&  \
    pip install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT