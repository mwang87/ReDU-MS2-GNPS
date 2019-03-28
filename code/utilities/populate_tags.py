
import sys
sys.path.insert(0, "..")

from models import *
from collections import defaultdict
import csv

def load_compound_tag_mapping(tag_mapping_filename):
    compound_map = defaultdict(list)
    with open(tag_mapping_filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            compound_name = row["GNPS_annotation"]
            tag1 = "Source0_" + row["Source"]
            tag2 = "Source1_" + row["Source_Sub1"]
            tag3 = "Source2_" + row["Source_Sub2"]

            if len(row["Source"]) > 2:
                compound_map[compound_name].append(tag1)

            if len(row["Source_Sub1"]) > 2:
                compound_map[compound_name].append(tag2)

            if len(row["Source_Sub2"]) > 2:
                compound_map[compound_name].append(tag3)

    return compound_map

def main():
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    Compound.create_table(True)
    CompoundFilenameConnection.create_table(True)
    FilenameAttributeConnection.create_table(True)
    CompoundTag.create_table(True)
    CompoundTagFilenameConnection.create_table(True)

    input_identifications = sys.argv[1]
    input_tags_mapping = sys.argv[2]

    tag_mapping = load_compound_tag_mapping(input_tags_mapping)

    all_files_in_db = Filename.select()
    all_files_in_db_set = set([filename.filepath for filename in all_files_in_db])

    processed_key = set()

    with open(input_identifications) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        line_count = 0
        for row in reader:
            line_count += 1

            if line_count % 1000 == 0:
                print(line_count)
            try:
                original_path = "f." + row["full_CCMS_path"]

                if not original_path in all_files_in_db_set:
                    continue

                key = original_path + ":" + row["Compound_Name"]

                if key in processed_key:
                    continue

                tags_for_compound = tag_mapping[row["Compound_Name"]]

                if len(tags_for_compound) > 0:
                    for tag in tags_for_compound:
                        if len(tag) > 2:
                            filename_db = Filename.get(filepath=original_path)
                            tag_db, status = CompoundTag.get_or_create(tagname=tag)
                            join_db = CompoundTagFilenameConnection.get_or_create(filename=filename_db, compoundtag=tag_db)

                processed_key.add(key)
            except KeyboardInterrupt:
                raise
            except:
                print("ERROR")
                raise
                continue




if __name__ == '__main__':
    main()
