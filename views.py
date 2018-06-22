# views.py
from flask import abort, jsonify, render_template, request, redirect, url_for

from app import app
from models import *

import json
import requests

"""Resolving ontologies only if they need to be"""
def resolve_ontology(attribute, term):
    if attribute == "ATTRIBUTE_BodyPart":
        url = "https://www.ebi.ac.uk/ols/api/ontologies/uberon/terms?iri=http://purl.obolibrary.org/obo/%s" % (term.replace(":", "_"))
        try:
            ontology_json = requests.get(url).json()
            print(json.dumps(ontology_json))
            return ontology_json["_embedded"]["terms"][0]["label"]
        except:
            return term

    if attribute == "ATTRIBUTE_Disease":
        url = "https://www.ebi.ac.uk/ols/api/ontologies/doid/terms?iri=http://purl.obolibrary.org/obo/%s" % (term.replace(":", "_"))
        try:
            ontology_json = requests.get(url).json()
            print(json.dumps(ontology_json))
            return ontology_json["_embedded"]["terms"][0]["label"]
        except:
            return term

    return term

@app.route('/', methods=['GET'])
def homepage():
    return redirect(url_for('dashboard'))

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
        output_dict["attributename"] = attribute.categoryname
        output_dict["countterms"] = len(all_terms)
        output_list.append(output_dict)

    return json.dumps(output_list)

#Returns all the terms given an attribute along with file counts for each term
@app.route('/attribute/<attribute>/attributeterms', methods=['GET'])
def viewattributeterms(attribute):
    attribute_db = Attribute.select().where(Attribute.categoryname == attribute)
    all_terms_db = AttributeTerm.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attribute == attribute_db).group_by(AttributeTerm.term)

    filters_list = json.loads(request.args['filters'])

    output_list = []

    for attribute_term_db in all_terms_db:
        all_files_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == attribute_term_db).where(FilenameAttributeConnection.attribute == attribute)
        all_files = set([file_db.filepath for file_db in all_files_db])
        #Adding the filter
        all_filtered_files_list = [all_files]
        for filterobject in filters_list:
            new_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == filterobject["attributeterm"]).where(FilenameAttributeConnection.attribute == filterobject["attributename"])
            print(attribute_term_db.term, len(new_db))

            all_filtered_files_list.append(set([file_db.filepath for file_db in new_db]))

        intersection_set = set.intersection(*all_filtered_files_list)



        #print(attribute_term_db.term, len(all_files_db))
        output_dict = {}
        output_dict["attributename"] = attribute
        output_dict["attributeterm"] = attribute_term_db.term
        output_dict["ontologyterm"] = resolve_ontology(attribute, attribute_term_db.term)
        output_dict["countfiles"] = len(intersection_set)
        output_list.append(output_dict)

    return json.dumps(output_list)

#Returns all the terms given an attribute along with file counts for each term
@app.route('/attribute/<attribute>/attributeterm/<term>/files', methods=['GET'])
def viewfilesattributeattributeterm(attribute, term):
    all_files_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == term).where(FilenameAttributeConnection.attribute == attribute)
    all_files = set([file_db.filepath for file_db in all_files_db])

    filters_list = json.loads(request.args['filters'])
    all_filtered_files_list = [all_files]
    for filterobject in filters_list:
        new_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == filterobject["attributeterm"]).where(FilenameAttributeConnection.attribute == filterobject["attributename"])

        all_filtered_files_list.append(set([file_db.filepath for file_db in new_db]))
    intersection_set = set.intersection(*all_filtered_files_list)

    output_list = []

    for filepath in intersection_set:
        output_dict = {}
        output_dict["attribute"] = attribute
        output_dict["attributeterm"] = term
        output_dict["filename"] = filepath
        output_list.append(output_dict)

    return json.dumps(output_list)

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "{'status' : 'up'}"


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/metadatabrowser', methods=['GET'])
def metadatabrowser():
    return render_template('metadatabrowser.html')
