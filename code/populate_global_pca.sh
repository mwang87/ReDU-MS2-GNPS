#This script syncs down the compound occurrences for all files and then shoves it into the database

ID_FILENAME=global_occurrences.tsv
TASKID=058564829a434277a5899f92fe4825a9
wget "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=$TASKID&block=main&file=compound_filename_occurences/" --output-document $ID_FILENAME
python3 ./redu_pca.py $ID_FILENAME $ID_FILENAME global.png
rm $ID_FILENAME