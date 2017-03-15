FROM python:2.7-alpine
MAINTAINER Marco Cotrufo <marco.cotrufo@devncode.it>

COPY . /code
EXPOSE 8000

WORKDIR /code
RUN apk add --no-cache mariadb-dev alpine-sdk && \
    pip install -r requirements.txt

VOLUME ["/code/static", "/code/logs"]

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "./gunicorn.conf", "euoserver.wsgi:application"]
