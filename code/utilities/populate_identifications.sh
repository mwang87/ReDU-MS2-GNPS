#!/bin/bash
#This script syncs down the identifications for all files and then shoves it into the database

python3 ./populate_identifications_libsearch.py /app/database/all_identifications.tsv --tasks /app/database/global_tasks.tsv