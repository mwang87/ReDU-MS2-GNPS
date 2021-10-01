#!/bin/bash

source activate py3

#export FLASK_ENV=development
#python3 ./main.py

gunicorn -w 2 -b 0.0.0.0:5001 --timeout 3600 main:app --access-logfile /app/logs/access.log