#!/bin/bash

while true; do
    cd utilities
    python ./search_dataset_metadata.py all
    cd ..
    python ./dump_all_metadata.py
    sleep 10m
done
