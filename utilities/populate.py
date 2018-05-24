
import sys
sys.path.insert(0, "..")

from models import *

import ming_fileio_library
import ming_proteosafe_library
import credentials

def resolve_metadata_filename_to_all_files(metadata_filename, all_files):
    stripped_extension = ming_fileio_library.get_filename_without_extension(metadata_filename)

    acceptable_filenames = ["f." + dataset_filename for dataset_filename in all_files if dataset_filename.find(stripped_extension) != -1]

    if len(acceptable_filenames) != 1:
        return None

    return acceptable_filenames[0]

def main():
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    FilenameAttributeConnection.create_table(True)

    dataset_accession = sys.argv[1]
    input_metadata_filename = sys.argv[2]

    result_list = ming_fileio_library.parse_table_with_headers_object_list(input_metadata_filename, "\t")

    ###Make sure we line these datasets up
    all_files = ming_proteosafe_library.get_all_files_in_dataset_folder(dataset_accession, "ccms_peak", credentials.USERNAME, credentials.PASSWORD)

    for result in result_list:
        filename = result["filename"].rstrip()
        dataset_filename = resolve_metadata_filename_to_all_files(filename, all_files)

        if dataset_filename == None:
            print(filename, "Not Found in Dataset")
            continue
        else:
            print(filename, "Found in Dataset")

        filename_db, status = Filename.get_or_create(filepath=dataset_filename)

        for key in result:
            if key.find("ATTRIBUTE_") != -1:
                attribute_name = key
                attribute_value = result[key]

                attribute_db, status = Attribute.get_or_create(categoryname=attribute_name)
                attribute_value_db, status = AttributeTerm.get_or_create(term=attribute_value)

                join_db = FilenameAttributeConnection.get_or_create(filename=filename_db, attribute=attribute_db, attributeterm=attribute_value_db)




if __name__ == '__main__':
    main()
