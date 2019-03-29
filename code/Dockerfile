FROM ubuntu:16.04
MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install urllib3==1.23
RUN pip install peewee
RUN pip install flask
RUN pip install requests
RUN pip install requests-cache
RUN pip install gunicorn
RUN pip install xmltodict
RUN pip install ftputil
RUN pip install vladiate
RUN pip install pandas

RUN apt-get install -y wget

#RUN apt-get update -y
#RUN export DEBIAN_FRONTEND=noninteractive
#RUN apt-get install -y r-base r-base-dev

COPY . /app
WORKDIR /app
