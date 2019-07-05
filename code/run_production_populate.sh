#!/bin/bash


cd utilities
python3 ./search_dataset_metadata.py all
sh ./populate_identifications.sh
cd ..
