#!/bin/bash
cd utilities
while true; do
    python3 ./populate_database.py \
    --importmetadata all \
    --importidentifications /app/database/global_tasks.tsv \
    --identifications_output /app/database/all_identifications.tsv >> /app/database/populate_metadata.log
    
    # Actually dumping everything into a file
    python3 ./dump_all_metadata.py
    cp ./all_sampleinformation.tsv /app/database/all_sampleinformation.tsv
    
    sleep 1800
done
