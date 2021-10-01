FROM continuumio/miniconda3:4.10.3
MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y && apt-get install -y build-essential git-core wget

RUN conda create -n py3 python=3.6.9

COPY requirements.txt . 
RUN /bin/bash -c "source activate py3 && pip install -r requirements.txt"
RUN /bin/bash -c "source activate py3 && pip install git+https://github.com/mwang87/CCMS_ProteoSAFe_pythonAPI.git"

COPY . /app
WORKDIR /app
