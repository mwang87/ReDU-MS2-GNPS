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

@app.route('/filename', methods=['GET'])
def getfilename():
    query_filename = request.args["query"]

    filepath_db = Filename.select().where(Filename.filepath == query_filename)

    if len(filepath_db) == 0:
        return "{}"

    all_terms = AttributeTerm.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.filename == filepath_db)


    return json.dumps([myterm.term for myterm in all_terms])
