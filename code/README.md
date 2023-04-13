**GNPS Metadata Tools** <br>
This repository contains three Python scripts for working with GNPS metadata files: _gnps_downloader.py_, _gnps_validator.py_, and _gnps_name_matcher.py_. These scripts allow you to aggregate lists of GNPS metadata files, validate the files using the GNPS metadata validator, and match the files to their respective CCMS peak dataset names.<br>

**Installation**<br>
To use these scripts, you'll need to have Python 3 installed on your system. <br>
You can download Python from the official Python website: https://www.python.org/downloads/<br>

-> You can install dependencies using pip:<br>
_pip install pandas urllib requests_<br>
<br>
**Usage**<br>
_**gnps_downloader.py**_<br>
This script aggregates a list of GNPS metadata files, sorts the files by their creation time, and downloads the latest GNPS metadata file. The script then appends the file path and file name into a TSV file.<br>

To run the script, use the following command: <br>
_python3 gnps_downloader.py_

_**gnps_validator.py**_<br>
This script runs the downloaded GNPS metadata files against the metadata validator and stores the list of file names that have passed through the validator. The script also rejects files that haven't passed and appends the passed file names into a TSV file.

To run the script, use the following command:<br>
_python3 gnps_validator.py_

_**gnps_name_matcher.py**_<br>
This script matches the GNPS metadata files to their respective CCMS peak dataset names and gives out a TSV file that contains all the names that match unambiguously.

To run the script, use the following command:<br>
_python3 gnps_name_matcher.py_
