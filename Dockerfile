#!/bin/bash
FROM --platform=linux/amd64 python:3.11.4-slim

ARG PORT
ENV DEBUG=0

WORKDIR tmp/project

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]