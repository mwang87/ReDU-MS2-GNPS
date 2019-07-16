#!/bin/bash

while true; do
    python3 ./dump_all_metadata.py
    cd utilities
    python3 ./search_dataset_metadata.py all
    cd ..
    python3 ./dump_all_metadata.py
    cp ./all_sampleinformation.tsv /app/temp/all_sampleinformation.tsv
    sleep 10m
done
