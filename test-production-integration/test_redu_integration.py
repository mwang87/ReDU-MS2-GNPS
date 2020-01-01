import os
import sys
import requests
import json

SERVER_URL = os.environ.get("SERVER_URL", "https://redu.ucsd.edu")
SAMPLE_TASK_ID = "ffa003f6c4d844188f1f751d34c649b0"
TEST_COMPOUND = "2,5-Dimethoxyphenethylamine"

def test_heartbeat():
    url = f"{SERVER_URL}/heartbeat"
    r = requests.get(url)
    r.raise_for_status()


def test_pca_library_search():
    query_url = f"{SERVER_URL}/processcomparemultivariate?task=f39c94cb7afe4568950bf61cdb8fee0d"
    r = requests.get(query_url)
    r.raise_for_status()

    return 0

def test_pca_metabolomics_snets():
    query_url = f"{SERVER_URL}/processcomparemultivariate?task=1ad7bc366aef45ce81d2dfcca0a9a5e7"
    r = requests.get(query_url)
    r.raise_for_status()

    return 0

def test_pca_feature_based():
    query_url = f"{SERVER_URL}/processcomparemultivariate?task=bb49a839face44cbb5ec3e6f855e7285"
    r = requests.get(query_url)
    r.raise_for_status()

    return 0


def test_data_dump():
    query_url = f"{SERVER_URL}/dump"
    response = requests.get(query_url)
    data = response.content
    file_size = sys.getsizeof(data)
    
    if file_size < 17762000:
        return 1

    return 0

def test_attribute_filtration():
    attribute = "ATTRIBUTE_DatasetAccession"
    query_url = f"{SERVER_URL}/attribute/{attribute}/attributeterms?filters=%%5B%%5D"
    response = requests.get(query_url)
    response.raise_for_status()

    #data = json.loads(response.content)
   # key_value = list(data[0].keys())
   # expected_keys = ["attributename", "attributeterm", "ontologyterm", "countfiles"]

    #if (key_value != expected_keys):
    #    return 1

    #return 0


def test_attribute_terms_display():
    query_url = f"{SERVER_URL}/attributes/"
    response = requests.get(query_url)
    data = json.loads(response.content)
    key_value = list(data[0].keys())

    expected_keys = ["attributename", "attributedisplay", "countterms"]

    if (key_value != expected_keys):
        return 1

    return 0

def test_file_enrichment():
    query_url = f"{SERVER_URL}/compoundfilename"
    params = {'compoundname' :  TEST_COMPOUND}
    response = requests.get(query_url, params = params)
    data = json.loads(response.content)

    key_value = next(iter(data[0]))

    if (key_value != 'filepath'):
       return 1
       
    return 0

def test_compound_enrichment():
    query_url = f"{SERVER_URL}/compoundenrichment"
    params = {'compoundname' : TEST_COMPOUND}
    response = requests.post(query_url, params )
    data = json.loads(response.content)  
    key_value = list(data[0].keys())
   
    expected_keys = ["attribute_name", "attribute_term", "totalfiles", "compoundfiles", "percentage"]
    
    if key_value != expected_keys:
        return 1
   
    return 0

def test_your_pca():
    params = {'task': SAMPLE_TASK_ID}
    query_url = f"{SERVER_URL}/processcomparemultivariate"
    response = requests.get(query_url, params = params)
    data = response.content
    file_size = sys.getsizeof(data) 
      
    if (file_size < 28000000):
       return 1

    return 0


def test_global_pca():
    query_url = f"{SERVER_URL}/displayglobalmultivariate"
    response = requests.get(query_url)
    data = response.content
    file_size = sys.getsizeof(data)    

    if (file_size < 27760000):
        return 1
    
    return 0
