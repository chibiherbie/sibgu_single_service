FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install pip-tools && pip install -r requirements.txt