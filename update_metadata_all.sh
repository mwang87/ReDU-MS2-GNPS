cd utilities
while true; do
    python ./search_dataset_metadata.py all >>update_metadata.log 2>&1
    sleep 5
done
