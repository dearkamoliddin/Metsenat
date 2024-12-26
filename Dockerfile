FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/

COPY ./requirements/develop.txt /app/requirements/develop.txt
COPY ./requirements/base.txt /app/requirements/base.txt

#RUN pip install --upgrade pip
RUN pip install -r /app/requirements/develop.txt

EXPOSE 8000
