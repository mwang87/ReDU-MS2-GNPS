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

ccms_peak_link_start = "https://gnps-datasetcache.ucsd.edu/datasette/database/filename.csv?_sort=filepath&collection__exact=ccms_peak&dataset__exact="
ccms_peak_link_end = "&_size=max"    
name = ""             
os.system("echo CCMS Read Done!")
current_dir = os.getcwd()
ccms_filenames = collections.defaultdict(set)
# print(current_dir)
if True:
    # Read the TSV file and specify the delimiter as a tab
    df = pd.read_csv(current_dir + '/passed_file_names.tsv', delimiter='\t', header=None, names=['Name'])
    # Extract the names from a specific column (e.g., column 'Name')
    passed_file_names = df['Name'].tolist()


    os.system("echo Iterating though rows now")
    merged_rows = {}
    # unique = 0
    # dupli = 0

    visit = set()
    for file in passed_file_names:
        # print("Length of visit is ",len(visit))
        print("Working on ", file)
        # os.system("echo Working on")
        # csv_path = os.path.join(current_dir, './data.csv' file)
        df = pd.read_csv( current_dir + "/" +file, delimiter='\t')
        try:            
            # Get the value of the first row of the 'column_name' column
            dataset = df['MassiveID'].iloc[0]

            ccms_df = pd.read_csv(ccms_peak_link_start + dataset + ccms_peak_link_end)
        except TypeError:
            print(f"Skipping file {file} due to a TypeError.")
            continue     
        for index, row in ccms_df.iterrows():
                # dataset = row["dataset"]
                filepath = row["filepath"]
                ccms_filenames[dataset].add(filepath)
        
        for index, row in df.iterrows():
            filename = row["filename"]
            filename2 = row["filename"][:-3] + "ML"
            for key in ccms_filenames[dataset]:
                if key.endswith(filename) or key.endswith(filename2):
                    if key in visit:
                        #  dupli += 1
                         merged_rows[key] = []
                    else:
                        #  unique += 1
                         visit.add(key)
                         new_row = [key] + list(row)
                         merged_rows[key] = list(new_row)
        print("Worked on ", file)
    os.system("echo Merged Rows list complete")
    non_empty_values = [v for v in merged_rows.values() if v]
    print("Length of Entries in Final file -> ",len(non_empty_values))

    # Read the TSV file containing headers into a pandas DataFrame
    # header_df = pd.read_csv(passed_file_names[-1], delimiter='\t', header=None)

    # Convert the values in the first row to a list
    # headers = header_df.iloc[0].tolist()

    # Create a DataFrame from the list with headers
    # fnt = pd.DataFrame(non_empty_values, columns=headers)
    fnt = pd.DataFrame(non_empty_values)
    # Save the DataFrame to a TSV file without column names
    # fnt.to_csv('check.tsv', sep='\t', index=False)
    fnt.to_csv('check.tsv', sep='\t', header = False, index=False)
    # print("Total Unique Entries are ",unique)
    # print("Duplicate Entries are ",dupli)


