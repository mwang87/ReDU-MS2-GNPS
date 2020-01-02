#!/bin/bash
cd utilities
while true; do
    python3 ./dump_all_metadata.py
    cp ./all_sampleinformation.tsv /app/database/all_sampleinformation.tsv
    python3 ./search_dataset_metadata.py all
    python3 ./dump_all_metadata.py
    cp ./all_sampleinformation.tsv /app/database/all_sampleinformation.tsv
    sleep 1800
done
