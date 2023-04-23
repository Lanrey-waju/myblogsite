# pull official base image
FROM python:3.11.3-alpine3.17

LABEL maintainer="Abdulmumin"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy required files
COPY ./requirements.txt /requirements.txt
COPY ./app /app

# set work directory
WORKDIR /app

# expose port
EXPOSE 8000

# Create virtual environment, install dependencies and add user
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home lanrey

ENV PATH="/py/bin/:$PATH"

USER lanrey

# copy project
COPY . .