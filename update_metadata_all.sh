cd utilities
while true; do
    python ./search_dataset_metadata.py all
    python ./dump_all_metadata.py
    sleep 10m
done
