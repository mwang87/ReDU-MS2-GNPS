import sys
#sys.path.insert(0, "..")
from collections import defaultdict
import json
import pandas as pd
import util
import credentials
from models import *

def main():
    all_filenames = list(Filename.select())

    task_id_list = []

    PARALLISM = 10
    for i in range(PARALLISM):
        partition_filenames = all_filenames[i::PARALLISM]
        
        filenames_list = [filename.filepath for filename in partition_filenames]

        taskid = util.launch_GNPS_librarysearchworkflow(filenames_list, "ReDU-MS2 Global Analysis Populate %i of %i" % (i, PARALLISM), \
            credentials.USERNAME, credentials.PASSWORD, "miw023@ucsd.edu")

        task_id_list.append(taskid)

    df = pd.DataFrame()
    df["taskid"] = task_id_list
    df.to_csv("./database/global_tasks.tsv", sep="\t", index=False)

if __name__ == '__main__':
    main()
