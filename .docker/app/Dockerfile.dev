FROM python:3.9-slim

WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary dependencies (PostgreSQL development libraries)
RUN apt-get update && apt-get install -y libpq-dev gcc

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY .. .