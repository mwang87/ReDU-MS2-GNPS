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
# ccms_df = pd.read_csv(ccms_peak_link_start + name + ccms_peak_link_end)
os.system("echo CCMS Read Done!")

ccms_filenames = collections.defaultdict(set)
# os.system("echo Creating Dictionary with Dataset -> filepath names ...")
# t = 0
# for index, row in ccms_df.iterrows():
#     dataset = row["dataset"]
#     filepath = row["filepath"]
#     ccms_filenames[dataset].add(filepath)

#     t += 1
    # print(row["filepath"], row["dataset"])
# print(len(ccms_filenames))

#Names of ccms_peak paths
# ccms_peak_list = ccms_df['filepath'].tolist()
# os.system("echo CCMS_Peak list generated ... ")
#<------------------------------------------------------->#
# print("Total entries are ",t)
# os.system("echo Dictionary Creation done!")

# continue
if True:
    # Read the TSV file and specify the delimiter as a tab
    df = pd.read_csv('passed_file_names.tsv', delimiter='\t', header=None, names=['Name'])
    # Extract the names from a specific column (e.g., column 'Name')
    passed_file_names = df['Name'].tolist()

    # Print the list of names
    # print(names_list)

    os.system("echo Iterating though rows now")
    merged_rows = {}
    unique = 0
    dupli = 0

    visit = set()
    for file in passed_file_names:
        print("Length of visit is ",len(visit))
        if file == "211_gnps_metadata.tsv":
             continue
        print("Working on ", file)
        # os.system("echo Working on")
        df = pd.read_csv(file, delimiter='\t')

        # Get the value of the first row of the 'column_name' column
        dataset = df['MassiveID'].iloc[0]
        
        # Print the value
        # print(dataset)
        ccms_df = pd.read_csv(ccms_peak_link_start + dataset + ccms_peak_link_end)
        for index, row in ccms_df.iterrows():
                # dataset = row["dataset"]
                filepath = row["filepath"]
                ccms_filenames[dataset].add(filepath)
                # t += 1
                # Total Entries are 1,32,313
        
        for index, row in df.iterrows():
            #<-------#>
            # dataset = row["MassiveID"]
            # ccms_df = pd.read_csv(ccms_peak_link_start + dataset + ccms_peak_link_end)
            # for index, row in ccms_df.iterrows():
            #     dataset = row["dataset"]
            #     filepath = row["filepath"]
            #     ccms_filenames[dataset].add(filepath)
            #<-------#>


            filename = row["filename"]
            filename2 = row["filename"][:-3] + "ML"
            for key in ccms_filenames[dataset]:
                if key.endswith(filename) or key.endswith(filename2):
                    if key in visit:
                         dupli += 1
                         merged_rows[key] = []
                    else:
                         unique += 1
                         visit.add(key)
                         new_row = [key] + list(row)
                            # rows.append(new_row)
                         merged_rows[key] = list(new_row)
                        #  extra_col = pd.DataFrame({'filename' : [key]})
                        #  merged_row = pd.concat([extra_col, row.to_frame().T], axis=1)
                        #  merged_row.to_csv('merged.tsv', mode='a', header=False, sep='\t', index=False)
                        #  print(f"{key} ends with {filename}")
                         
                    # if filename or filename2 
                    # Add the merged row to the list of merged rows
                    
                    # print("hello")

                # else:
                    # print(f"{key} does not end with {filename}")
                    # print()
        print("Worked on ", file)
    os.system("echo Merged Rows list complete")
    non_empty_values = [v for v in merged_rows.values() if v]
    print("The length is " , len(non_empty_values))
    # Create a DataFrame from the list
    fnt = pd.DataFrame(non_empty_values)

    # Save the DataFrame to a TSV file without column names
    fnt.to_csv('check.tsv', sep='\t', header=False, index=False)
    # read first TSV file with a header into a pandas dataframe
    # df1 = pd.read_csv('f.tsv', delimiter='\t')
    # output_df = pd.concat(merged_rows, ignore_index=True)
    # output_df.to_csv('MERGED.tsv', sep='\t', index=False)
    # os.system("echo Merged File created !")
    print("Total Unique Entries are ",unique)
    print("Duplicate Entries are ",dupli)



#^^^^^^^^

    # # Create an empty data frame to store the merged data
    # merged_df = pd.DataFrame()

    # # Loop through each file and concatenate it to the merged data frame
    # for file in passed_file_names:
    #     df = pd.read_csv(file, delimiter='\t')
    #     merged_df = pd.concat([merged_df, df], axis=0)

    # # Write the merged data frame to a new TSV file
    # merged_df.to_csv('merged.tsv', sep='\t', index=False)

    #<------------------------------------------------------->#

    # os.system("python3 metadata_validator.py 10_gnps_metadata.tsv")
    # proc = subprocess.Popen(["python3", "metadata_validator.py 10_gnps_metadata.tsv"], stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    # print("program output:", out)


    # var = os.popen('python3 metadata_validator.py 10_gnps_metadata.tsv').read()
    # if var[0] == "S":
    #     print("my var is ",var)