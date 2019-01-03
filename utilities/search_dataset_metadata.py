
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


def find_dataset_metadata(dataset_accession):
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

def main():
    dataset_accession = "MSV000080673"
    dataset_metadatum = find_dataset_metadata(dataset_accession)
    print(dataset_metadatum)
    #Save files Locally
    local_metadata_path = os.path.join("tempuploads", dataset_accession + ".tsv")
    ftp_path = "ftp://massive.ucsd.edu/" + dataset_metadatum["path"]
    import urllib
    urllib.urlretrieve(ftp_path, local_metadata_path)
    #Validate
    pass_validation, failures, errors_list = metadata_validator.perform_validation(local_metadata_path)
    #print(pass_validation, errors_list)

    #Filtering out lines
    local_filtered_metadata_path = os.path.join("tempuploads", "filtered_" + dataset_accession + ".tsv")
    if len([error for error in errors_list if error["error_string"].find("Missing column") != -1]) > 0:
        print("Missing Columns, Rejected")
        exit(0)

    no_validation_lines = [int(error["line_number"]) for error in errors_list]
    no_validation_lines.sort()

    with open(local_filtered_metadata_path, "w") as filtered_file:
        line_count = 0
        for line in open(local_metadata_path):
            line_count += 1
            if line_count in no_validation_lines:
                continue
            filtered_file.write(line)

    pass_validation, failures, errors_list = metadata_validator.perform_validation(local_filtered_metadata_path)
    populate.populate_dataset_metadata(local_filtered_metadata_path)

    #print(pass_validation, errors_list)








    # all_datasets = ming_proteosafe_library.get_all_datasets()
    #
    # for dataset in all_datasets:
    #     if dataset["title"].find("GNPS") == -1:
    #         continue
    #     find_dataset_metadata(dataset["dataset"])



if __name__ == "__main__":
    main()
