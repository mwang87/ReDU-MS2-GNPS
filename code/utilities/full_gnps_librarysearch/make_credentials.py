#!/usr/bin/python

#This makes the credientials file

import sys
import os
import json

def usage():
    print("<server url> <username> <password> <output credentials file>")


def main():
    server_url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    credentials = {}
    credentials["server_url"] = server_url
    credentials["username"] = username
    credentials["password"] = password

    output_credentials_file = "credentials.json"

    try:
        output_credentials_file = sys.argv[4]
    except:
        print("No credentials file given, writing to credentials.json")

    open(output_credentials_file, "w").write(json.dumps(credentials,indent = 4))


if __name__ == "__main__":
    main()
