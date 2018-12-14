#!/usr/bin/python

#This executable loads the job submissions in JSON and submits them one by one

import sys
import getopt
import os
import json
import time
import uuid
import requests
import argparse
import copy
import csv

def get_all_datasets(gnps_only=False):
    SERVER_URL = "http://gnps.ucsd.edu/ProteoSAFe/datasets_json.jsp"

    url = SERVER_URL
    r = requests.get(url)
    json_object = json.loads(r.text)

    if gnps_only == True:
        gnps_datasets = [dataset for dataset in json_object["datasets"] if dataset["title"].upper().find("GNPS") != -1]
        return gnps_datasets

    return json_object["datasets"]

def invoke_workflow(credentials, parameters):
    s = requests.Session()

    login = {
        'user' : credentials['username'],
        'password' : credentials['password'],
        'login' : 'Sign in'
    }

    r_login = s.post('http://{}/ProteoSAFe/user/login.jsp'.format(credentials['server_url']), data=login)
    r_login.status_code
    r_login.raise_for_status()

    r_invoke = s.post('http://{}/ProteoSAFe/InvokeTools'.format(credentials['server_url']), data=parameters)
    r_invoke.raise_for_status()

    task_id = r_invoke.text

    print(task_id)

    if len(task_id) > 4 and len(task_id) < 60:
        print("Launched Task: {}".format(task_id))
        return task_id
    else:
        return None

def run_all_jobs_delayed(params_list, sleep_time, credentials):
    job_ids = []
    for param_object in params_list:
        task_id = invoke_workflow(credentials, param_object)
        job_object = {}
        job_object["description"] = param_object["desc"][0]
        job_object["task"] = task_id
        job_ids.append(job_object)
        time.sleep(sleep_time)
    return job_ids

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('credentialsjson', default="credentials.json", help='credentialsjson')
    parser.add_argument('jobparamsjson', help='jobparamsjson')
    parser.add_argument('inputfilesparametertoreplace', help='Input Files Parameter to Replace')
    parser.add_argument('outputtaskscsv', help='Output tasks csv')
    parser.add_argument('outputtasksjson', help='Output tasks json')
    args = parser.parse_args()

    valid_file_extensions = ["mzXML","mzML","mzML.gz","mgf"]

    credentials = json.loads(open(args.credentialsjson).read())
    workflow_parameters = json.loads(open(args.jobparamsjson).read())


    #Loading all GNPS datasets
    all_gnps_datasets = get_all_datasets(gnps_only=True)[:10]
    submission_parameters = []
    for dataset in all_gnps_datasets:
        dataset_accession = dataset["dataset"]
        path_to_peaks = "d.%s/ccms_peak;" % (dataset_accession)

        search_parameters = copy.deepcopy(workflow_parameters)
        search_parameters[args.inputfilesparametertoreplace][0] = path_to_peaks
        search_parameters["desc"][0] = "%s MetaAnalysis - %s" % (dataset_accession, dataset["title"])

        submission_parameters.append(search_parameters)

    all_jobs = run_all_jobs_delayed(submission_parameters, 0, credentials)

    with open(args.outputtaskscsv, 'w') as csvfile:
        fieldnames = ['description', 'task']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for job in all_jobs:
            writer.writerow(job)

    with open(args.outputtasksjson, 'w') as jsonfile:
        jsonfile.write(json.dumps(all_jobs))

    exit(0)

if __name__ == "__main__":
    main()
