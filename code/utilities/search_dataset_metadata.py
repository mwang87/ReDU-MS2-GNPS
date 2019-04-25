
import sys
sys.path.insert(0, "..")

from collections import defaultdict

from app import db
import os
import metadata_validator
import ming_fileio_library
import ming_proteosafe_library
import populate
import credentials
import ftputil
import pandas as pd

massive_host = ftputil.FTPHost("massive.ucsd.edu", "anonymous", "")

def find_dataset_metadata(dataset_accession, useftp=False):
    print("Finding Files %s " % dataset_accession)
    if useftp:
        all_other_files = []
        #all_other_files = ming_proteosafe_library.get_all_files_in_dataset_folder_ftp(dataset_accession, "other", includefilemetadata=True, massive_host=massive_host)
        all_update_files = ming_proteosafe_library.get_all_files_in_dataset_folder_ftp(dataset_accession, "updates", includefilemetadata=True, massive_host=massive_host)
    else:
        all_other_files = ming_proteosafe_library.get_all_files_in_dataset_folder(dataset_accession, "other", credentials.USERNAME, credentials.PASSWORD, includefilemetadata=True)
        all_update_files = ming_proteosafe_library.get_all_files_in_dataset_folder(dataset_accession, "updates", credentials.USERNAME, credentials.PASSWORD, includefilemetadata=True)

    print(dataset_accession, len(all_other_files), len(all_update_files))

    #Finding gnps_metadata.tsv files
    metadata_files = [fileobject for fileobject in all_other_files if os.path.basename(fileobject["path"]) == "gnps_metadata.tsv" ]
    metadata_files += [fileobject for fileobject in all_update_files if os.path.basename(fileobject["path"]) == "gnps_metadata.tsv" ]

    metadata_files = sorted(metadata_files, key=lambda myfile: myfile["timestamp"], reverse=True)

    if len(metadata_files) > 0:
        return metadata_files[0]

    return None

def process_metadata_import(dataset_accession):
    dataset_metadatum = find_dataset_metadata(dataset_accession, useftp=True)

    if dataset_metadatum == None:
        print("Not Importing %s, no metadata" % dataset_accession)
        return
    else:
        print("Importing %s" % dataset_accession, dataset_metadatum)

    #Save files Locally
    local_metadata_path = os.path.join("tempuploads", dataset_accession + ".tsv")

    try:
        massive_host.download(dataset_metadatum["path"], local_metadata_path)
    except:
        print("CANT DOWNLOAD", dataset_metadatum["path"])
        raise

    """
    Metadata Fields Rewrite

    Fields changed and will need to be rewritten

    """

    metadata_df = pd.read_csv(local_metadata_path, sep="\t")

    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='anal region',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='adrenal gland',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='brain',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='caecum',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='cardiac vein',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='colon',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='coronary artery',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='duodenum',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='esophagus',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='gall bladder',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='heart',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='ileum',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='jejunum',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='kidney',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='liver',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='lung',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='midgut',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='nasal cavity',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='oral cavity',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='ovary',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='pancreas',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='pulmonary artery',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='pulmonary vein',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='skin',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='spleen',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='sputum',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='stomach',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='thymus',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='tooth',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='trachea',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='uterine cervix',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='uterus',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='vagina',value='tissue',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='bile',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='blood',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='blood plasma',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='blood serum',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='breast milk',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='feces',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='saliva',value='biofluid',inplace=True)
    metadata_df['ATTRIBUTE_Curated_SampleType_Sub1'].replace(to_replace='urine',value='biofluid',inplace=True)

    #Rewriting Year of Analysis
    metadata_list = metadata_df.to_dict(orient="records")
    for metadata_obj in metadata_list:
        try:
            metadata_obj["Analysis_YearOfAnalysis"] = str(int(float(metadata_obj["Analysis_YearOfAnalysis"])))
        except:
            continue

    metadata_df = pd.DataFrame(metadata_list)
    metadata_df.to_csv(local_metadata_path, sep="\t", index=False)

    
    #Validate
    pass_validation, failures, errors_list, valid_rows, total_rows_count = metadata_validator.perform_validation(local_metadata_path)

    #Filtering out lines that are not valid
    local_filtered_metadata_path = os.path.join("tempuploads", "filtered_" + dataset_accession + ".tsv")
    if len([error for error in errors_list if error["error_string"].find("Missing column") != -1]) > 0:
        print("Missing Columns, Rejected")
        return

    pd.DataFrame(valid_rows).to_csv(local_filtered_metadata_path, sep="\t", index=False)

    try:
        pass_validation, failures, errors_list, valid_rows, total_rows_count = metadata_validator.perform_validation(local_filtered_metadata_path)
    except:
        pass_validation = False

    if pass_validation:
        print("Importing Data")
        populate.populate_dataset_metadata(local_filtered_metadata_path)
    else:
        print("Filtered File is not valid")


def main():
    mode = sys.argv[1]
    if mode == "all":
        all_datasets = ming_proteosafe_library.get_all_datasets()
        for dataset in all_datasets:
            if dataset["title"].find("GNPS") == -1:
                continue
            process_metadata_import(dataset["dataset"])
    elif mode == "dataset":
        dataset_accession = sys.argv[2]
        process_metadata_import(dataset_accession)


if __name__ == "__main__":
    main()
