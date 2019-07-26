
import sys
import os
import argparse
sys.path.insert(0, "..")

from models import *
from collections import defaultdict
import csv
import requests
import pandas as pd

def main():
    input_identifications = sys.argv[1]

    parser = argparse.ArgumentParser(description='Importing Identification Data')
    parser.add_argument('input_identifications', help='Identifications Filename')
    parser.add_argument('--tasks', default=None, help='List of GNPS Tasks for Library ID')

    args = parser.parse_args()

    #Checking that the input identiifcations are present
    if not os.path.isfile(args.input_identifications):
        #Identifications is missing
        if args.tasks != None:
            print("Downloading Identifications")
            df = pd.read_csv(args.tasks, sep="\t")
            all_tasks = df.to_dict(orient="records")
            all_data_df = []
            for task in all_tasks:
                print(task)
                taskid = task["taskid"]
                url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=DB_result/" % (taskid)
                data_df = pd.read_csv(url, sep="\t")
                print(taskid, len(data_df))
                all_data_df.append(data_df)

            merged_df = pd.concat(all_data_df)
            merged_df.to_csv(args.input_identifications, sep="\t", index=False)

    #Actually Populating the Data
    all_files_in_db = Filename.select()
    all_files_in_db_set = set([filename.filepath for filename in all_files_in_db])

    processed_key = set()

    with open(input_identifications) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        line_count = 0
        for row in reader:
            line_count += 1

            if line_count % 1000 == 0:
                print(line_count)

            try:
                original_path = "f." + row["full_CCMS_path"]

                if not original_path in all_files_in_db_set:
                    continue

                key = original_path + ":" + row["Compound_Name"]

                if key in processed_key:
                    continue

                filename_db = Filename.get(filepath=original_path)
                compound_db, status = Compound.get_or_create(compoundname=row['Compound_Name'])
                join_db = CompoundFilenameConnection.get_or_create(filename=filename_db, compound=compound_db)

                processed_key.add(key)
            except KeyboardInterrupt:
                raise
            except:
                print("ERROR")
                continue




if __name__ == '__main__':
    main()
