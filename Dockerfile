FROM python:2.7-alpine
MAINTAINER Marco Cotrufo <marco.cotrufo@devncode.it>

COPY . /code
EXPOSE 8000

WORKDIR /code
RUN apk update && apk add mariadb-dev alpine-sdk && \
    pip install -r requirements.txt

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "./gunicorn.conf", "--log-config", "./logging.conf", "euoserver.wsgi:application"]
