
import sys
sys.path.insert(0, "..")

from models import *
from collections import defaultdict

import ming_fileio_library
import ming_proteosafe_library
import credentials

all_datasets = ming_proteosafe_library.get_all_datasets()


for dataset in all_datasets:
    if dataset["title"].find("GNPS") == -1:
        continue

    all_other_files = ming_proteosafe_library.get_all_files_in_dataset_folder(dataset["dataset"], "other", credentials.USERNAME, credentials.PASSWORD)
    all_update_files = ming_proteosafe_library.get_all_files_in_dataset_folder(dataset["dataset"], "updates", credentials.USERNAME, credentials.PASSWORD)

    print(dataset["dataset"], len(all_other_files), len(all_update_files))


    for filename in all_other_files:
        print(filename)

    for filename in all_update_files:
        print(filename)
