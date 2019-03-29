#!/bin/bash


cd utilities
python ./search_dataset_metadata.py all
sh ./populate_identifications.sh
cd ..
