#!/usr/bin/python

#This executable loads the job submissions in JSON and submits them one by one

import sys
import getopt
import os
import json
import argparse
import copy
import csv
from functools import reduce
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('foldertomerge', help='foldertomerge')
    parser.add_argument('outputtsv', help='outputtsv')
    args = parser.parse_args()

    all_files_to_merge = [os.path.join(args.foldertomerge, filename) for filename in os.listdir(args.foldertomerge)]
    all_files_to_merge.sort()

    df_final = pd.DataFrame({"full_CCMS_path" : [], "Compound_Name" : []})
    dfs = []
    for filename in all_files_to_merge:
        try:
            print(filename)
            pandas_table = pd.read_table(filename, sep="\t")[["full_CCMS_path", "Compound_Name"]]

            pandas_table["full_CCMS_path"] = pandas_table["full_CCMS_path"].apply(lambda path: "f." + path)
            pandas_table = pandas_table.drop_duplicates()

            df_final = df_final.merge(pandas_table, how="outer")
            #dfs.append(pandas_table)
        except KeyboardInterrupt:
            raise
        except:
            #raise
            print("Error Loading")

    #print("Merging DF")
    #df_final = reduce(lambda left,right: pd.merge(left,right,how='outer'), dfs)

    print("Writing DF")
    df_final.to_csv(args.outputtsv, index = False, sep="\t")

    exit(0)

if __name__ == "__main__":
    main()
