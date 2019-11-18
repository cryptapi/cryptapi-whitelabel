FROM httpd:2.4

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing

RUN apt-get install -y apt-utils

RUN apt-get update --fix-missing

RUN apt-get install -y apache2-dev wget tar git python3 python3-dev python3-pip libapache2-mod-wsgi-py3 cron postgresql-client

RUN mkdir /conf
ADD . /conf
WORKDIR /conf

RUN mkdir -p /var/certs/

COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY cert.pem /var/certs/cert.pem
COPY cert.key /var/certs/cert.key

COPY run-apache /usr/local/bin/run-apache
RUN chmod +x /usr/local/bin/run-apache

RUN pip3 install -r requirements.txt

WORKDIR /data

ENV DEBIAN_FRONTEND teletype