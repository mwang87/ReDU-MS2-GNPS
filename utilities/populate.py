
import sys
sys.path.insert(0, "..")

from models import *

import ming_fileio_library

def main():
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)

    result_list = ming_fileio_library.parse_table_with_headers_object_list(sys.argv[1], ",")


    for result in result_list:
        filename = result["Filename"].rstrip()
        filename_db = Filename.create(filepath=filename)


if __name__ == '__main__':
    main()
