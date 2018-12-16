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



    all_compounds = []

    merged_dict = {"filename" : [], "LibraryID" : []}
    for filename in all_files_to_merge:
        print(filename)
        try:
            pandas_table = pd.read_table(filename, index_col ="LibraryID", sep="\t")
            pandas_table = pandas_table.drop(['TotalFiles'], axis=1)

            df_dict = pandas_table.to_dict()
            for filename in df_dict:
                for library_id in df_dict[filename]:
                    if df_dict[filename][library_id]  > 0:
                        merged_dict["filename"].append(filename)
                        merged_dict["LibraryID"].append(library_id)
                #merged_dict[filename] = df_dict[filename]

            #dfs.append(pandas_table)
        except KeyboardInterrupt:
            raise
        except:
            #raise
            print("Error Loading")



    # for df in dfs:
    #     if len(df.to_dict()) > 0:
    #         all_compounds += list(df[df.keys()[0]].keys())
    #     all_compounds = list(set(all_compounds))
    #     print(len(all_compounds))
    #
    # new_dict = {}
    # for df in dfs:
    #     df_dict = df.to_dict()
    #     print(df_dict)
    #     for key in df_dict:
    #         filename_dict = {}
    #         for compound_name in all_compounds:
    #             if compound_name in df_dict[key]:
    #                 filename_dict[compound_name] = df_dict[key][compound_name]
    #         new_dict[key] = filename_dict
    #
    # for key in new_dict:
    #     print(new_dict[key])


    merged_df = pd.DataFrame.from_dict(merged_dict)
    #merged_df.index.name = "LibraryID"
    #merged_df['TotalFiles'] = merged_df.sum(axis=1)

    merged_df.to_csv(args.outputtsv, index = False, sep="\t")
    #print(new_dict.keys())




        #print(df.to_dict())

    #for df in dfs:


        #print(pandas_table.columns.values)

        #print("MING", pandas_table["Surugamide F"])

    #df_final = reduce(lambda left,right: pd.merge(left,right, how="outer", on="key"), dfs)
    #df_final = reduce(lambda left,right: pd.merge(left,right, how="outer"), dfs)
    #print(df_final)




if __name__ == "__main__":
    main()
