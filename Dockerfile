FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y chromium-browser
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 main:app
