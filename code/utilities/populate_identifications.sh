#This script syncs down the identifications for all files and then shoves it into the database


ID_FILENAME=all_identifications.tsv
TASKID=058564829a434277a5899f92fe4825a9
#TASKID=6aee538b5fbc4b9a83ee803a06330feb
wget "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=$TASKID&block=main&file=DB_result/" --output-document $ID_FILENAME
python ./populate_identifications_libsearch.py $ID_FILENAME
rm $ID_FILENAME
