#!/usr/bin/python


import sys
import os
import argparse
import csv
import json
from vladiate import Vlad
from vladiate.validators import UniqueValidator, SetValidator
from vladiate.inputs import LocalFile

def perform_validation(filename):
    validators = {
        'filename': [
            UniqueValidator()
        ]
    }

    my_validator = Vlad(source=LocalFile(filename),delimiter="\t",ignore_missing_validators=True,validators=validators)
    passes_validation = my_validator.validate()

    errors_list = []
    for column in my_validator.failures:
        for line_number in my_validator.failures[column]:
            error_dict = {}
            error_dict["header"] = column
            error_dict["line_number"] = line_number
            error_dict["error_string"] = str(my_validator.failures[column][line_number])

            errors_list.append(error_dict)


    return passes_validation, my_validator.failures, errors_list

def main():
    parser = argparse.ArgumentParser(description='Validate Stuff.')
    parser.add_argument('inputmetadata', help='inputmetadata')
    args = parser.parse_args()

    passes_validation, failures, errors_list = perform_validation(args.inputmetadata)



    #with open(args.inputmetadata, 'rb') as csvfile:
        #dialect = csv.Sniffer().sniff(csvfile.read(1024))
        #csvfile.seek(0)
        #reader = csv.DictReader(csvfile, dialect=dialect)
        #for row in reader:
        #    print(row)

if __name__ == "__main__":
    main()
