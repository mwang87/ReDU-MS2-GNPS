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



def test_data_dump():
    query_url = f"{SERVER_URL}/dump"
    response = requests.get(query_url)
    data = response.content
    file_size = sys.getsizeof(data)

    assert(file_size > 17762000)

def test_attribute_filtration():
    attribute = "ATTRIBUTE_DatasetAccession"
    query_url = f"{SERVER_URL}/attribute/{attribute}/attributeterms?filters=[]"
    response = requests.get(query_url)
    response.raise_for_status()


def test_attribute_terms_fields():
    query_url = f"{SERVER_URL}/attributes"
    response = requests.get(query_url)
    data = response.json()
    key_value = list(data[0].keys())

    expected_keys = ["attributename", "attributedisplay", "countterms"]

    assert(key_value == expected_keys)

def test_attribute_list():
    query_url = f"{SERVER_URL}/attributes"
    r = requests.get(query_url)
    all_attributes = r.json()
    for attribute in all_attributes:
        attribute_name = attribute["attributename"]
        query_url = f"{SERVER_URL}/attribute/{attribute_name}/attributeterms?filters=[]"
        response = requests.get(query_url)
        response.raise_for_status()
        

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

    assert(expected_keys == key_value)


def test_pca_library_search():
    query_url = f"{SERVER_URL}/processcomparemultivariate?task=f39c94cb7afe4568950bf61cdb8fee0d"
    r = requests.get(query_url)
    r.raise_for_status()

def test_pca_metabolomics_snets():
    query_url = f"{SERVER_URL}/processcomparemultivariate?task=1ad7bc366aef45ce81d2dfcca0a9a5e7"
    r = requests.get(query_url)
    r.raise_for_status()

def test_pca_feature_based():
    query_url = f"{SERVER_URL}/processcomparemultivariate?task=bb49a839face44cbb5ec3e6f855e7285"
    r = requests.get(query_url)
    r.raise_for_status()

def test_your_pca():
    params = {'task': SAMPLE_TASK_ID}
    query_url = f"{SERVER_URL}/processcomparemultivariate"
    response = requests.get(query_url, params = params)
    data = response.content
    file_size = sys.getsizeof(data)
    
    assert(file_size > 22000000)


def test_global_pca():
    query_url = f"{SERVER_URL}/displayglobalmultivariate"
    response = requests.get(query_url)
    data = response.content
    file_size = sys.getsizeof(data)

    assert(file_size > 22760000)


def testing_massive_api():
    url = "https://massive.ucsd.edu/ProteoSAFe//proxi/v0.1/datasets?filter=MSV000084741&function=datasets"
    r = requests.get(url)
    r.json()
    r.raise_for_status()


def test_groups_comparison():
    url = f"{SERVER_URL}/explorer"
    params = {'G1' : json.dumps(["f.MSV000082490/ccms_peak/mzXML/Samples/Skin/SH793_RA5_01_27710.mzML"]), 
    'G2' : "[]",
    'G3' : "[]",
    'G4' : "[]",
    'G5' : "[]",
    'G6' : "[]"
    }
    r = requests.post(url, data=params)
    r.raise_for_status()