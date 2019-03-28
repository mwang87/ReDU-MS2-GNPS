
import sys
sys.path.insert(0, "..")

from models import *
from collections import defaultdict
import csv

def main():
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    Compound.create_table(True)
    CompoundFilenameConnection.create_table(True)
    FilenameAttributeConnection.create_table(True)

    input_identifications = sys.argv[1]

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

                filename_db = Filename.get(filepath=original_path)
                compound_db, status = Compound.get_or_create(compoundname=row['Compound_Name'])
                join_db = CompoundFilenameConnection.get_or_create(filename=filename_db, compound=compound_db)

                processed_key.add(key)
            except KeyboardInterrupt:
                raise
            except:
                print("ERROR")
                continue




if __name__ == '__main__':
    main()
