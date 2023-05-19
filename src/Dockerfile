FROM python:3.10.4-slim

COPY .. /app
WORKDIR /app

RUN python3 -m  venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade &&  \
    /opt/venv/bin/pip install -r requirements.txt

RUN sh -c "chmod +x /app/migrate.sh && \
     sh /app/migrate.sh && \
     /opt/venv/bin/gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"