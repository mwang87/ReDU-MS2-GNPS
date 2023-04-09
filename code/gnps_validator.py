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

# Print message to indicate importing is done
os.system("echo Importing Done ...")
current_dir = os.getcwd()
# Read the TSV file containing file paths into a pandas DataFrame
df = pd.read_csv(current_dir + '/file_paths.tsv', delimiter='\t')

# Get a list of all the values in the first column (file names)
file_names = df.iloc[:, 0].tolist()

# List to store names of files that have passed validation
passed_file_names = []

# Loop through each file in the list of file names and validate each one
os.system("echo Validating Files now ...")
for file_name in file_names:
    # Call the metadata_validator.py script and pass the file name as an argument
    output = os.popen("python3 /Users/siddhantpoojary/Desktop/ReDU-MS2-GNPS/code/metadata_validator.py " + current_dir +'/' + file_name).read()
    # If the script output starts with "S", then the file has passed validation
    if output and output[0] == "S":
        passed_file_names.append(file_name)

# Print message to indicate that validation is complete
os.system("echo Validation Completed !")

# Convert the list of passed file names to a pandas DataFrame
passed = pd.DataFrame(passed_file_names)
 
# Print message to indicate that a TSV file is being created for path names
os.system("echo Now creating tsv file for Path names ...")

# Write the passed file names DataFrame to a TSV file
passed.to_csv('passed_file_names.tsv', sep='\t', index=False, header=False)

# Print message to indicate that the TSV file has been created and the script is complete
os.system("echo TSV File created! Have a good day.")
