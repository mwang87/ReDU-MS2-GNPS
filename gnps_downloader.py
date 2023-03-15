import os
import pandas as pd
import urllib
import requests
import io 
import sys
import collections
import argparse
from pandas.errors import EmptyDataError
os.system("echo Importing Done!")
gnps_metadata_link = "https://gnps-datasetcache.ucsd.edu/database/filename.csv?_sort=filepath&filepath__endswith=gnps_metadata.tsv&_size=max"
# ccms_peak_link = "https://gnps-datasetcache.ucsd.edu/database/filename.csv?_sort=filepath&collection__contains=ccms&_size=max"

gnps_df = pd.read_csv(gnps_metadata_link)
os.system("echo GNPS CSV Read Done!")

# Convert the create time column to a datetime format
gnps_df['create_time'] = pd.to_datetime(gnps_df['create_time'])

# Sort the DataFrame by the create time column
gnps_df = gnps_df.sort_values(by='create_time')

# Group the DataFrame by the dataset column
groups = gnps_df.groupby('dataset')

# Select the row with the highest create time value for each group
selected_rows = []
for name, group in groups:
    idx = group['create_time'].idxmax()
    selected_rows.append(group.loc[idx])



# Names of GNPS Files
# gnps_list = gnps_df['filepath'].tolist()
gnps_list = [row['filepath'] for row in selected_rows]
print("Total gnps file are ", len(gnps_list))
os.system("echo Filepath list generated ... ")
# gnps_list[:5]




download_link = "https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?forceDownload=true&file=f."
os.system("echo We are downloading now ...")

# count = len(gnps_list) #Limiting to 5
file_paths = collections.defaultdict(list)
for index, link in enumerate(gnps_list):
  download_url = download_link + link
  r = requests.get(download_url)
  file_name = str(index) + "_gnps_metadata.tsv"
  # file_paths[file_name] = link # Dictionary for file paths
  file_paths["sys_name"].append(file_name)
  file_paths["svr_name"].append(link)
  with open(file_name,'wb') as f:
    f.write(r.content) #Downloading
os.system("echo Download has been completed successfully!")

os.system("echo Creating tsv for file paths ...")
with open("file_paths.tsv", "w") as f:
  f.write("LocalName\tServerName\n")
  for i in range(len(file_paths["sys_name"])):
    local = file_paths["sys_name"][i]
    server = file_paths["svr_name"][i]
    f.write(f"{local}\t{server}\n")
  f.close()
os.system("echo Tsv file created for path names!")
os.system("echo EXECUTION COMPLETE ! HAVE A GOOD DAY ")





# c = 0

# for i in range(909): #Limiting to 310
  # if i == 850:
  #   continue
  # name = str(i) + "_gnps_metadata.tsv"
  # try:
  #   df = pd.read_csv(name, sep ='\t', encoding= 'unicode_escape')
  # except EmptyDataError:
  #   continue
  # try:
  #   gnps_file_name = df['filename'].iloc[0]
  #   # print (i)
  # except KeyError:
  #   try:
  #     gnps_file_name = df['Filename'].iloc[0]
  #     # print (i)
  #   except:
  #     continue
  # for key in ccms_peak_file_names:
  #   n = len(gnps_file_name)
  #   if key[-n:] == gnps_file_name:
  #     ccms_peak_file_names[key].append(gnps_file_name)
  #     c += 1
  #     break

# for v in ccms_peak_file_names.values():
#   if not v:
#     continue
#   print (v)

# validator_path = "/content/ReDU-MS2-GNPS/code/metadata_validator.py"

# os.system("python3 metadata_validator.py 556_gnps_metadata.tsv")
# dummy_read = pd.read_csv("10_gnps_metadata.tsv", sep ='\t', encoding= 'unicode_escape')
# parser = argparse.ArgumentParser(description='Parsing one file')
# parser.add_argument("10_gnps_metadata.tsv")



# for i in range(909):
# name = str(i) + "_gnps_metadata.tsv"
# !python3 "/content/ReDU-MS2-GNPS/code/metadata_validator.py" 556_gnps_metadata.tsv