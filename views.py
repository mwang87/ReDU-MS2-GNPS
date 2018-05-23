# views.py
from flask import abort, jsonify, render_template, request

from app import app
from models import *

import json

@app.route('/', methods=['GET'])
def homepage():
    files = Filename.select()

    print([myfile.filepath for myfile in files])
    return json.dumps([myfile.filepath for myfile in files])
