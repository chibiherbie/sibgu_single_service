FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

#RUN mkdir /core

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install pip-tools && pip install -r requirements.txt
#RUN apt-get update && apt-get install gcc libpq-dev python3-dev -y && apt-get autoclean