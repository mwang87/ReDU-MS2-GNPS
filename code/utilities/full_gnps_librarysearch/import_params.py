#!/usr/bin/python

import xmltodict
import sys
import json
import requests
from collections import defaultdict

def import_params_to_dict(server_url, task_id):
    params = {}
    full_url = "https://" + server_url + "/ProteoSAFe/ManageParameters"
    response = requests.get(full_url, params={"task" : task_id})

    response_text = response.text
    params = xmltodict.parse(response_text)

    print(json.dumps(params,indent = 4))

    return params

def filter_params(params,blacklist):
    parameters = params['parameters']['parameter']

    new_parameters = defaultdict(list)
    for parameter in parameters:
        param_name = parameter["@name"]
        param_value = parameter["#text"]

        if param_name not in blacklist:
            new_parameters[param_name].append(param_value)

    return new_parameters

def usage():
    print("<server url e.g. proteomics.ucsd.edu> <task> <output json file>")

def main():
    blacklist = {
        'task',
        'upload_file_mapping',
        'uuid',
        'user',
        'reanalyzed_datasets'
    }

    server_url = sys.argv[1]
    task_id = sys.argv[2]
    output_json_filename = sys.argv[3]

    params = import_params_to_dict(server_url, task_id)
    params = filter_params(params,blacklist)
    print(json.dumps(params,indent = 4))
    open(output_json_filename, "w").write(json.dumps(params,indent = 4))

if __name__ == '__main__':
    main()
