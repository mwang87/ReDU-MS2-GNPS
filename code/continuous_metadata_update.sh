#!/bin/bash

while true; do
    python ./dump_all_metadata.py
    cd utilities
    python ./search_dataset_metadata.py all
    cd ..
    python ./dump_all_metadata.py
    sleep 10m
done
