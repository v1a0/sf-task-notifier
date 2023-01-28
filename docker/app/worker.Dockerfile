FROM python:3.11.1-bullseye
WORKDIR /app/notifier
COPY . /app

RUN pip3 --disable-pip-version-check --no-cache-dir install  -r /app/requirements.txt
