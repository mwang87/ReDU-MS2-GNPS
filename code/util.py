import ming_proteosafe_library

def launch_GNPS_librarysearchworkflow(files_list, job_description, username, password, email):
    invokeParameters = {}
    invokeParameters["workflow"] = "MOLECULAR-LIBRARYSEARCH-V2"
    invokeParameters["protocol"] = "None"
    invokeParameters["desc"] = job_description
    invokeParameters["library_on_server"] = "d.speclibs;"
    invokeParameters["spec_on_server"] = ";".join(files_list)
    invokeParameters["tolerance.PM_tolerance"] = "2.0"
    invokeParameters["tolerance.Ion_tolerance"] = "0.5"

    invokeParameters["MIN_MATCHED_PEAKS"] = "6"
    invokeParameters["TOP_K_RESULTS"] = "1"

    invokeParameters["FILTER_STDDEV_PEAK_datasetsINT"] = "0.0"
    invokeParameters["MIN_PEAK_INT"] = "0.0"
    invokeParameters["FILTER_PRECURSOR_WINDOW"] = "1"
    invokeParameters["FILTER_LIBRARY"] = "1"
    invokeParameters["WINDOW_FILTER"] = "1"

    invokeParameters["SEARCH_LIBQUALITY"] = "3"

    invokeParameters["MAX_SHIFT_MASS"] = "100.0"
    invokeParameters["ANALOG_SEARCH"] = "0"
    invokeParameters["SCORE_THRESHOLD"] = "0.7"

    invokeParameters["email"] = email
    invokeParameters["uuid"] = "1DCE40F7-1211-0001-979D-15DAB2D0B500"

    task_id = ming_proteosafe_library.invoke_workflow("gnps.ucsd.edu", invokeParameters, username, password)

    return task_id
