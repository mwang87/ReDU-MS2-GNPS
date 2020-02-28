import sys
import glob
sys.path.insert(0, "../code/")
import metadata_validator

def test_valid():
    valid_files = glob.glob("data/validator/valid*")
    for valid_filename in valid_files:
        print(valid_filename)
        passes_validation, failures, errors_list, valid_rows, row_count = metadata_validator.perform_validation(valid_filename)
        assert(passes_validation is True)

def test_invalid():
    invalid_files = glob.glob("data/validator/invalid*")
    for invalid_filename in invalid_files:
        print(invalid_filename)
        passes_validation, failures, errors_list, valid_rows, row_count = metadata_validator.perform_validation(invalid_filename)
        assert(passes_validation is False)
