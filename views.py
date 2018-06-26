# views.py
from flask import abort, jsonify, render_template, request, redirect, url_for

from app import app
from models import *

import json
import requests
import requests_cache

requests_cache.install_cache('demo_cache', allowable_codes=(200, 404, 500))

"""Resolving ontologies only if they need to be"""
def resolve_ontology(attribute, term):
    if attribute == "ATTRIBUTE_BodyPart":
        url = "https://www.ebi.ac.uk/ols/api/ontologies/uberon/terms?iri=http://purl.obolibrary.org/obo/%s" % (term.replace(":", "_"))
        print(url)
        try:
            ontology_json = requests.get(url).json()
            #print(json.dumps(ontology_json))
            return ontology_json["_embedded"]["terms"][0]["label"]
        except KeyboardInterrupt:
            raise
        except:
            return term

    if attribute == "ATTRIBUTE_Disease":
        url = "https://www.ebi.ac.uk/ols/api/ontologies/doid/terms?iri=http://purl.obolibrary.org/obo/%s" % (term.replace(":", "_"))
        print(url)
        try:
            ontology_json = requests.get(url).json()
            #print(json.dumps(ontology_json))
            return ontology_json["_embedded"]["terms"][0]["label"]
        except KeyboardInterrupt:
            raise
        except:
            return term

    return term

def count_compounds_in_files(filelist1, filelist2, filelist3, filelist4, filelist5, filelist6):
    output_list = []
    input_fileset1 = set(filelist1)
    input_fileset2 = set(filelist2)
    input_fileset3 = set(filelist3)
    input_fileset4 = set(filelist4)
    input_fileset5 = set(filelist5)
    input_fileset6 = set(filelist6)

    all_compounds = Compound.select()
    for my_compound in all_compounds:
        my_files = Filename.select().join(CompoundFilenameConnection).where(CompoundFilenameConnection.compound==my_compound)
        my_files_set = set([one_file.filepath for one_file in my_files])
        intersection_set1 = input_fileset1.intersection(my_files_set)
        intersection_set2 = input_fileset2.intersection(my_files_set)
        intersection_set3 = input_fileset3.intersection(my_files_set)
        intersection_set4 = input_fileset4.intersection(my_files_set)
        intersection_set5 = input_fileset5.intersection(my_files_set)
        intersection_set6 = input_fileset6.intersection(my_files_set)

        output_dict = {}
        output_dict["compound"] = my_compound.compoundname

        output_dict["count1"] = len(intersection_set1)
        if len(filelist1) > 0:
            output_dict["count1_norm"] = int(float(len(intersection_set1)) / float(len(filelist1)) * 100.0)
        else:
            output_dict["count1_norm"] = 0

        output_dict["count2"] = len(intersection_set2)
        if len(filelist2) > 0:
            output_dict["count2_norm"] = int(float(len(intersection_set2)) / float(len(filelist2)) * 100.0)
        else:
            output_dict["count2_norm"] = 0

        output_dict["count3"] = len(intersection_set3)
        if len(filelist3) > 0:
            output_dict["count3_norm"] = int(float(len(intersection_set3)) / float(len(filelist3)) * 100.0)
        else:
            output_dict["count3_norm"] = 0

        output_dict["count4"] = len(intersection_set4)
        if len(filelist4) > 0:
            output_dict["count4_norm"] = int(float(len(intersection_set4)) / float(len(filelist4)) * 100.0)
        else:
            output_dict["count4_norm"] = 0

        output_dict["count5"] = len(intersection_set5)
        if len(filelist5) > 0:
            output_dict["count5_norm"] = int(float(len(intersection_set5)) / float(len(filelist5)) * 100.0)
        else:
            output_dict["count5_norm"] = 0

        output_dict["count6"] = len(intersection_set6)
        if len(filelist6) > 0:
            output_dict["count6_norm"] = int(float(len(intersection_set6)) / float(len(filelist6)) * 100.0)
        else:
            output_dict["count6_norm"] = 0

        output_list.append(output_dict)

    return output_list

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

#Summarize Files Per Comparison Group
@app.route('/explorer', methods=['POST'])
def summarizefiles():
    all_files_G1 = json.loads(request.form["G1"])
    all_files_G2 = json.loads(request.form["G2"])
    all_files_G3 = json.loads(request.form["G3"])
    all_files_G4 = json.loads(request.form["G4"])
    all_files_G5 = json.loads(request.form["G5"])
    all_files_G6 = json.loads(request.form["G6"])

    output = count_compounds_in_files(all_files_G1, all_files_G2, all_files_G3, all_files_G4, all_files_G5, all_files_G6)

    return json.dumps(output)

#Summarize Files Per Comparison Group
@app.route('/explorerdashboard', methods=['GET'])
def explorerdashboard():
    return render_template('explorerdashboard.html')

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "{'status' : 'up'}"

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/metadatabrowser', methods=['GET'])
def metadatabrowser():
    return render_template('metadatabrowser.html')
