FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /phonebook-app

RUN apk update
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /phonebook-app/requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/phonebook-app/src"

LABEL maintainer="paralepsis <der.krabbentaucher@gmail.com>"