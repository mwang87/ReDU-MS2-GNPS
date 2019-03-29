#!/bin/bash

gunicorn --daemon -w 4 -b 0.0.0.0:5001 --timeout 3600 main:app
sh ./continuous_metadata_update.sh >>update_metadata.log 2>&1
