
import sys
sys.path.insert(0, "..")

from models import *

import ming_fileio_library

def main():
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    FilenameAttributeConnection.create_table(True)

    result_list = ming_fileio_library.parse_table_with_headers_object_list(sys.argv[1], ",")


    for result in result_list:
        filename = result["Filename"].rstrip()
        filename_db, status = Filename.get_or_create(filepath=filename)

        for key in result:
            if key.find("ATTRIBUTE_") != -1:
                attribute_name = key
                attribute_value = result[key]

                attribute_db, status = Attribute.get_or_create(categoryname=attribute_name)
                attribute_value_db, status = AttributeTerm.get_or_create(term=attribute_value)

                join_db = FilenameAttributeConnection.get_or_create(filename=filename_db, attribute=attribute_db, attributeterm=attribute_value_db)




if __name__ == '__main__':
    main()
