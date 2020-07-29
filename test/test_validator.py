import sys
import glob
sys.path.insert(0, "../code/")
import metadata_validator

def test_valid():
    valid_files = glob.glob("data/validator/valid_*")
    for valid_filename in valid_files:
        passes_validation, failures, errors_list, valid_rows, row_count = metadata_validator.perform_validation(valid_filename)
        dataset_success, result_string, matched_dataset_items = metadata_validator.perform_validation_against_massive(valid_filename)
        print("VALIDATION", valid_filename, "VALID ROWS", len(valid_rows), "TOTAL ROWS", row_count, dataset_success, "TOTAL MASSIVE VALID ROWS", matched_dataset_items)
        assert(passes_validation is True)
        assert(matched_dataset_items == len(valid_rows))
        assert(matched_dataset_items == row_count)

def test_invalid():
    invalid_files = glob.glob("data/validator/invalid_*")
    for invalid_filename in invalid_files:
        print(invalid_filename)
        passes_validation, failures, errors_list, valid_rows, row_count = metadata_validator.perform_validation(invalid_filename)
        assert(passes_validation is False)

def test_invalid_massive():
    invalid_files = glob.glob("data/validator/invaliddata_*")
    for invalid_filename in invalid_files:
        print(invalid_filename)
        passes_validation, failures, errors_list, valid_rows, row_count = metadata_validator.perform_validation(invalid_filename)
        assert(passes_validation is True)
        dataset_success, result_string, matched_dataset_items = metadata_validator.perform_validation_against_massive(invalid_filename)
        assert(matched_dataset_items == 0)
