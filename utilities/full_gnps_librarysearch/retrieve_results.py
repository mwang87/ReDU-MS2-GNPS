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

import requests_cache

requests_cache.install_cache('demo_cache', allowable_codes=(200, 404, 500))


def get_task_information(base_url, task_id):
    url = 'https://' + base_url + '/ProteoSAFe/status_json.jsp?task=' + task_id
    return json.loads(requests.get(url, verify=False).text)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('credentialsjson', default="credentials.json", help='credentialsjson')
    parser.add_argument('tasksjson', default="tasks.json", help='tasksjson')
    parser.add_argument('gnpspathname', help='gnpspathname')
    parser.add_argument('outputdirectory', help='Output tasks json')
    args = parser.parse_args()

    credentials = json.loads(open(args.credentialsjson).read())
    all_jobs = json.loads(open(args.tasksjson).read())

    for job in all_jobs:
        task = job["task"]
        if task != None and len(task) == 32:
            task_information = get_task_information(credentials["server_url"], task)
            print(task_information["status"])
            if task_information["status"] == "DONE":
                retreival_url = "http://%s/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=%s" % (credentials["server_url"], task, args.gnpspathname)
                print(retreival_url)
                r = requests.get(retreival_url, allow_redirects=True)
                output_filename = os.path.join(args.outputdirectory, task)
                open(output_filename, 'wb').write(r.content)

    exit(0)

if __name__ == "__main__":
    main()
