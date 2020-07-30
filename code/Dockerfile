FROM ubuntu:18.04
MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

RUN pip3 install urllib3==1.23
RUN pip3 install peewee
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install requests-cache
RUN pip3 install gunicorn
RUN pip3 install xmltodict
RUN pip3 install ftputil
RUN pip3 install vladiate
RUN pip3 install pandas

RUN pip3 install matplotlib
RUN pip3 install scikit-bio
RUN pip3 install emperor==1.0.0b19 --pre

RUN apt-get install -y wget

RUN pip3 install sklearn
RUN pip3 install seaborn

RUN apt-get update -y
RUN apt-get install -y git-core
RUN pip3 install git+https://github.com/mwang87/CCMS_ProteoSAFe_pythonAPI.git
RUN pip3 install bokeh

COPY . /app
WORKDIR /app
