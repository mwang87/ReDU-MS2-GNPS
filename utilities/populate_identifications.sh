#This script syncs down the identifications for all files and then shoves it into the database

ID_FILENAME=all_identifications.tsv
wget "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=debed173fe98453dbb0cd10552fbc778&block=main&file=DB_result/" --output-document $ID_FILENAME
python ./populate_identifications_libsearch.py $ID_FILENAME
rm $ID_FILENAME
