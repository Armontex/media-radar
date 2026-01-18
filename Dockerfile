FROM python:3.12.3-slim

WORKDIR /usr/src/app

COPY . ./

RUN pip install -r requirements.txt