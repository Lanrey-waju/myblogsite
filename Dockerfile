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
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home lanrey && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R lanrey:lanrey /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin/:$PATH"

USER lanrey

