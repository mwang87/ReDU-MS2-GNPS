import os
import sys
import requests
import json

BASE_URL = "https://redu.ucsd.edu/"
URL_ONE = "displayglobalmultivariate"
URL_TWO = "processcomparemultivariate"
SAMPLE_TASK_ID = "ffa003f6c4d844188f1f751d34c649b0"
URL_THREE = "ReDUValidator" #optional
URL_FIVE = "compoundfilename"
TEST_COMPOUND = "2,5-Dimethoxyphenethylamine"
URL_SIX = "compoundenrichment"
URL_FOUR  = "/attributes"
URL_SEVEN = "attribute/MassSpectrometer/attributeterms?filters=%5B%5D"
URL_EIGHT = "dump"

def test_data_dump():
    query_url = BASE_URL + URL_EIGHT
    response = requests.get(query_url)
    data = response.content
    file_size = sys.getsizeof(data)
    
    if file_size < 17762000:
        sys.exit(1)
    else:
        sys.exit(0)

def test_attribute_filtration():
    query_url = BASE_URL + URL_SEVEN
    response = requests.get(query_url)
    data = json.loads(response.content)
    key_value = list(data[0].keys())
    print(key_value)
    expected_keys = ["attributename", "attributeterm", "ontologyterm", "countfiles"]

    if (key_value == expected_keys):
        sys.exit(0)
    else:
        sys.exit(1)


def test_attribute_terms_display():
    query_url = BASE_URL + URL_FOUR
    response = requests.get(query_url)
    data = json.loads(response.content)
    key_value = list(data[0].keys())

    expected_keys = ["attribute_name", "attributedisplay", "countterms"]

    if (key_value == expected_keys):
        sys.exit(0)

    else:
        sys.exit(1)


def test_file_enrichment():
    query_url = BASE_URL + URL_FIVE
    params = {'compoundname' :  TEST_COMPOUND}
    response = requests.get(query_url, params = params)
    data = json.loads(response.content)

    key_value = next(iter(data[0]))

    if (key_value == 'filepath'):
       sys.exit(0)
       
    else:
        sys.exit(1)

def test_compound_enrichment():
   query_url = BASE_URL + URL_SIX  
   params = {'compoundname' : TEST_COMPOUND}
   response = requests.post(query_url, params )
   data = json.loads(response.content)  
   key_value = list(data[0].keys())
   
   expected_keys = ["attribute_name", "attribute_term", "totalfiles", "compoundfiles", "percentage"]
    
   if key_value == expected_keys:
       sys.exit(0)
   else:
       sys.exit(1)

def test_your_pca():
   params = {'task': SAMPLE_TASK_ID}
   query_url = BASE_URL + URL_TWO
   response = requests.get(query_url, params = params)
   data = response.content
   file_size = sys.getsizeof(data) 
      
   if (file_size < 28000000):
       sys.exit(1)
   else: 
       sys.exit(0)   


def test_global_pca():
    response = requests.get(BASE_URL + URL_ONE)
    data = response.content
    file_size = sys.getsizeof(data)
            
    if (file_size < 27762100):
        sys.exit(1)
    
    else:
        sys.exit(0)

def main():
    test_attribute_filtration()

if __name__ == "__main__":
    main()
