#!/bin/bash
source activate py3

cd utilities
python3 ./populate_database.py --importmetadata dataset --metadataaccession MSV000083388
