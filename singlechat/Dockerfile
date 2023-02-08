FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /singlechat

WORKDIR /singlechat

COPY . /singlechat/

RUN pip install --upgrade pip && pip install pip-tools && pip install -r requirements.txt