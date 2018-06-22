FROM ubuntu:latest
MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install peewee
RUN pip install flask
RUN pip install requests
RUN pip install requests-cache

COPY . /app
WORKDIR /app
