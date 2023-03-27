FROM python:3.10-slim
LABEL maintainer="jus1stored@gmail.com"

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
