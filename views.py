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
        return "[]"

    all_terms = AttributeTerm.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.filename == filepath_db)


    return json.dumps([myterm.term for myterm in all_terms])

@app.route('/attributes', methods=['GET'])
def viewattributes():
    all_attributes = Attribute.select()

    output_list = []
    for attribute in all_attributes:
        all_terms = AttributeTerm.select().join(FilenameAttributeConnection).join(Attribute).where(Attribute.categoryname == attribute.categoryname).group_by(AttributeTerm.term)
        output_dict = {}
        output_dict["attribute"] = attribute.categoryname
        output_dict["countterms"] = len(all_terms)
        output_list.append(output_dict)

    return json.dumps(output_dict)

#Returns all the terms given an attribute along with file counts for each term
@app.route('/attribute/<attribute>/attributeterms', methods=['GET'])
def viewattributeterms(attribute):
    attribute_db = Attribute.select().where(Attribute.categoryname == attribute)
    all_terms_db = AttributeTerm.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attribute == attribute_db).group_by(AttributeTerm.term)

    output_list = []

    for attribute_term_db in all_terms_db:
        all_files_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == attribute_term_db.term).where(FilenameAttributeConnection.attribute == attribute_db)
        #print(attribute_term_db.term, len(all_files_db))
        output_dict = {}
        output_dict["attribute"] = attribute
        output_dict["attributeterm"] = attribute_term_db.term
        output_dict["countfiles"] = len(all_files_db)
        output_list.append(output_dict)

    return json.dumps(output_list)

#Returns all the terms given an attribute along with file counts for each term
@app.route('/attribute/<attribute>/attributeterm/<term>/files', methods=['GET'])
def viewfilesattributeattributeterm(attribute, term):
    all_files_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == term).where(FilenameAttributeConnection.attribute == attribute)

    output_list = []

    for file_db in all_files_db:
        output_dict = {}
        output_dict["attribute"] = attribute
        output_dict["attributeterm"] = term
        output_dict["filename"] = file_db.filepath
        output_list.append(output_dict)

    return json.dumps(output_list)

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "{'status' : 'up'}"
