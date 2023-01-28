FROM python:3.11-slim-bullseye
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ="Etc/UTC"
WORKDIR /app/notifier
COPY . /app

RUN apt-get update && apt-get install -y curl && apt-get clean

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /app/requirements.txt

