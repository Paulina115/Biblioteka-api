FROM python:3.12.7-alpine3.20

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache \
    postgresql-client \
    libpq \
    gcc \
    musl-dev \
    python3-dev \
    postgresql-dev \
    zlib-dev \
    linux-headers

RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /src
COPY ./src /src

RUN adduser -D user
USER user
