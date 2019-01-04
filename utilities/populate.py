
import sys
sys.path.insert(0, "..")
from collections import defaultdict
import json

from models import *
import ming_fileio_library
import ming_proteosafe_library
import metadata_validator
import credentials

try:
    import redis
    redis_client = redis.Redis()
except:
    print("no redis")



def get_dataset_files(dataset_accession, collection_name):
    dataset_files = None

    try:
        dataset_files = json.loads(redis_client.get(dataset_accession))
    except:
        dataset_files = None

    if dataset_files is None:
        dataset_files = ming_proteosafe_library.get_all_files_in_dataset_folder(dataset_accession, collection_name, credentials.USERNAME, credentials.PASSWORD)
        try:
            redis_client.set(dataset_accession, json.dumps(dataset_files))
        except:
            x = 1

    return dataset_files


def resolve_metadata_filename_to_all_files(filename, all_files):
    stripped_extension = ming_fileio_library.get_filename_without_extension(filename)

    acceptable_filenames = ["f." + dataset_filename for dataset_filename in all_files if dataset_filename.find(stripped_extension) != -1]

    if len(acceptable_filenames) != 1:
        return None

    return acceptable_filenames[0]

def add_metadata_per_accession(dataset_accession, metadata_list):
    whitelist_columns = ["Study_SubjectIdentifierAsRecorded",
    "Study_UniqueSubjectID",
    "ATTRIBUTE_Subject_Sex",
    "Subject_AgeInYears",
    "ATTRIBUTE_Subject_LifeStage",
    "Subject_Country",
    "ATTRIBUTE_Subject_HumanPopulationDensity",
    "Analysis_SampleCollectionMethod",
    "Analysis_SampleExtractionMethod",
    "Analysis_InternalStandardsUsed",
    "ATTRIBUTE_Analysis_MassSpectrometer",
    "Analysis_IonizationSourceAndPolarity",
    "Analysis_ChromatographyAndPhase",
    "Analysis_YearOfAnalysis",
    "Study_DayAsReported",
    "Study_DayRelative",
    "Study_TimepointMin",
    "Study_Health",
    "Study_SampleTypeasRecorded",
    "Study_SampleTermsofPosition",
    "ATTRIBUTE_Curated_SampleType",
    "ATTRIBUTE_Curated_SampleType_Sub1",
    "ATTRIBUTE_Curated_BodyPartOntologyName",
    "ATTRIBUTE_Curated_BodyPartOntologyIndex",
    "Curated_DiseaseCommonName",
    "ATTRIBUTE_Curated_DiseaseOntologyIndex",
    "Curated_Comorbidity_ListDOIDs"]

    added_files = 0

    ###Make sure we line these datasets up
    all_files = get_dataset_files(dataset_accession, "ccms_peak")

    for result in metadata_list:
        filename = result["filename"].rstrip()

        dataset_filename = resolve_metadata_filename_to_all_files(filename, all_files)

        if dataset_filename == None:
            continue

        added_files += 1

        filename_db, status = Filename.get_or_create(filepath=dataset_filename, datasetaccession=dataset_accession)

        #Adding Default Attribute of Dataset Accession
        attribute_db, status = Attribute.get_or_create(categoryname="ATTRIBUTE_DatasetAccession")
        attribute_value_db, status = AttributeTerm.get_or_create(term=dataset_accession)
        join_db = FilenameAttributeConnection.get_or_create(filename=filename_db, attribute=attribute_db, attributeterm=attribute_value_db)

        for key in result:
            if not key in whitelist_columns:
                continue

            attribute_name = key
            attribute_value = result[key]

            attribute_db, status = Attribute.get_or_create(categoryname=attribute_name)
            attribute_value_db, status = AttributeTerm.get_or_create(term=attribute_value)

            join_db = FilenameAttributeConnection.get_or_create(filename=filename_db, attribute=attribute_db, attributeterm=attribute_value_db)

    if added_files == 0:
        print(dataset_accession, "No Files Found")

    return added_files

def populate_dataset_metadata(input_metadata_filename):
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    Compound.create_table(True)
    CompoundFilenameConnection.create_table(True)
    FilenameAttributeConnection.create_table(True)
    CompoundTag.create_table(True)
    CompoundTagFilenameConnection.create_table(True)

    print(input_metadata_filename)

    result_list = ming_fileio_library.parse_table_with_headers_object_list(input_metadata_filename, "\t")

    metadata_by_accession = defaultdict(list)

    for result in result_list:
        massive_accession = result["MassiveID"]
        metadata_by_accession[massive_accession].append(result)

    for dataset_accession in metadata_by_accession:
        added_files = add_metadata_per_accession(dataset_accession, metadata_by_accession[dataset_accession])
        print(dataset_accession, len(metadata_by_accession[dataset_accession]), added_files)

def main():
    input_metadata_filename = sys.argv[1]
    populate_dataset_metadata(input_metadata_filename)









if __name__ == '__main__':
    main()
