import os 
import pandas as pd
import urllib
import requests
import io 
import sys
import argparse
import subprocess
import collections
from subprocess import PIPE, run
validator_path = "/content/ReDU-MS2-GNPS/code/metadata_validator.py"
dir_path = '/Users/siddhantpoojary/Desktop/ReDU-MS2-GNPS-master/code'
file_names = os.listdir(dir_path)
os.system("echo Importing Done ...")

#<------------------------------------------------------->#
# List of file names to merge
passed_file_names = []
os.system("echo Validating Files now ...")
# os.system("echo Limit is of 25 files as per now")
# c = 0
for file_name in file_names:
    if file_name.endswith("_gnps_metadata.tsv"):
        try:
            output = os.popen("python3 metadata_validator.py " + file_name).read()
        except ValueError:
            os.system("echo ValueError encountered! Skipping the file")
            continue
        if output and output[0] == "S":
            passed_file_names.append(file_name)
            # c += 1
        # if c == 30:
            # os.system("echo 10 HIT")
            # break

os.system("echo Validation Completed !")


# Convert the list of arrays to a pandas DataFrame
passed = pd.DataFrame(passed_file_names)
os.system("echo Now creating tsv file for Path names ...")
# Write the DataFrame to a TSV file
passed.to_csv('passed_file_names.tsv', sep='\t', index=False, header=False)

os.system("echo TSV File created! Have a good day.")

# with open('passed_file_names.tsv', 'w', newline='') as f:
#         writer = csv.writer(f, delimiter='\t')


#<------------------------------------------------------->#
