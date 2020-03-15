#!/bin/bash

cd utilities
python3 ./populate_database.py --importmetadata all \
    --importidentifications /app/database/global_tasks.tsv \
    --identifications_output /app/database/all_identifications.tsv
