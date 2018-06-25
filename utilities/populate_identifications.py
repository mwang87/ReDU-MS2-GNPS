
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

    #for filename in Filename.select():
    #    print(filename.filepath)

    with open(input_identifications) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        line_count = 0
        for row in reader:
            line_count += 1
            
            try:
                original_path = row["Original_Path"].replace("MSV000078556/spectrum", "MSV000078556/ccms_peak")
                if original_path.find("MSV000078556") == -1:
                    continue
                filename_db = Filename.get(filepath=original_path)
                print(row['Original_Path'])
                compound_db, status = Compound.get_or_create(compoundname=row['compound_name'])
                join_db = CompoundFilenameConnection.get_or_create(filename=filename_db, compound=compound_db)
            except KeyboardInterrupt:
                raise
            except:
                continue




if __name__ == '__main__':
    main()
