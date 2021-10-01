#!/bin/bash
#This script syncs down the identifications for all files and then shoves it into the database
source activate py3

cd utilities
python3 ./populate_database.py --importidentifications /app/database/global_tasks.tsv --identifications_output /app/database/all_identifications.tsv