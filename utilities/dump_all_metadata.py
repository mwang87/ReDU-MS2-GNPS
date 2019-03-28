
import sys
sys.path.insert(0, "..")
from collections import defaultdict
import json
import pandas as pd

from models import *

def main():
    all_file_metadata = []

    all_filenames = Filename.select()
    print(len(all_filenames))
    loop_count = 0
    for filename in all_filenames:
        resolved_terms = []
        file_metadata = {}
        file_metadata["filename"] = filename.filepath
        all_connections = FilenameAttributeConnection.select().where(FilenameAttributeConnection.filename == filename)
        for connection in all_connections:
            attribute_name = connection.attribute.categoryname
            attribute_term = connection.attributeterm.term

            resolved_terms.append({"attribute_name": attribute_name, "attribute_term" : attribute_term})
            file_metadata[attribute_name] = attribute_term.rstrip()

        all_file_metadata.append(file_metadata)

        loop_count += 1
        if loop_count % 100 == 0:
            print(loop_count, filename.filepath, len(resolved_terms))

    df = pd.DataFrame(all_file_metadata)
    df.to_csv("all_metadata_dumps.tsv", sep="\t")

if __name__ == '__main__':
    main()
