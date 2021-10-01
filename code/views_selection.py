from app import app
import json
import pandas as pd
from flask import request

import config
from ontology_utils import resolve_ontology

black_list_attribute = ["SubjectIdentifierAsRecorded", "UniqueSubjectID", "UBERONOntologyIndex", "DOIDOntologyIndex", "ComorbidityListDOIDIndex"]

##############################
# Metadata Selector API Calls
##############################
@app.route('/attributes', methods=['GET'])
def viewattributes():
    # Reading the dump instead of the database
    metadata_df = pd.read_csv(config.PATH_TO_ORIGINAL_MAPPING_FILE, sep="\t", dtype=str)

    all_attributes_list = list(metadata_df.columns)

    output_list = []
    for attribute in all_attributes_list:
        output_dict = {}
        output_dict["attributename"] = attribute
        output_dict["attributedisplay"] = attribute.replace("ATTRIBUTE_", "").replace("Analysis_", "").replace("Subject_", "").replace("Curated_", "")

        all_terms = set(metadata_df[attribute])
        output_dict["countterms"] = len(all_terms)

        if attribute == "filename":
            continue

        if attribute in black_list_attribute:
            continue
        else:
            output_list.append(output_dict)

    output_list = sorted(output_list, key=lambda x: x["attributedisplay"], reverse=False)

    return json.dumps(output_list)


#Returns all the terms given an attribute along with file counts for each term
@app.route('/attribute/<attribute>/attributeterms', methods=['GET'])
def viewattributeterms(attribute):
    metadata_df = pd.read_csv(config.PATH_TO_ORIGINAL_MAPPING_FILE, sep="\t", dtype=str)
    filters_list = json.loads(request.values.get('filters', "[]"))

    # Applying filters
    for filterobject in filters_list:
        filter_attribute = filterobject["attributename"]
        filter_term = filterobject["attributeterm"]

        #TODO: check for types
        metadata_df = metadata_df[metadata_df[filter_attribute] == filter_term]

    terms_list = list(set(metadata_df[attribute]))

    output_list = []
    grouped_term_df = metadata_df.groupby(attribute)
    for term, term_df in grouped_term_df:
        #term_df = metadata_df[metadata_df[attribute] == term]
        if len(term_df) > 0:
            output_dict = {}
            output_dict["attributename"] = attribute
            output_dict["attributeterm"] = term
            output_dict["ontologyterm"] = resolve_ontology(attribute, term)
            output_dict["countfiles"] = len(term_df)
            output_list.append(output_dict)

    return json.dumps(output_list)

#Returns all the terms given an attribute along with file counts for each term
@app.route('/attribute/<attribute>/attributeterm/<term>/files', methods=['GET'])
def viewfilesattributeattributeterm(attribute, term):
    metadata_df = pd.read_csv(config.PATH_TO_ORIGINAL_MAPPING_FILE, sep="\t", dtype=str)
    filters_list = json.loads(request.values.get('filters', "[]"))

    # Applying filters
    for filterobject in filters_list:
        filter_attribute = filterobject["attributename"]
        filter_term = filterobject["attributeterm"]

        #TODO: check for types
        metadata_df = metadata_df[metadata_df[filter_attribute] == filter_term]

    metadata_df = metadata_df[["filename", attribute]]
    metadata_df = metadata_df[metadata_df[attribute] == term]

    metadata_list = metadata_df.to_dict(orient="records")

    output_list = []
    for metadata_obj in metadata_list:
        output_dict = {}
        output_dict["attribute"] = attribute
        output_dict["attributeterm"] = term
        output_dict["filename"] = metadata_obj["filename"]
        output_list.append(output_dict)

    return json.dumps(output_list)

