
import uuid
import pandas as pd
import os
import json

from flask import send_file, request, render_template

#import redu_pca
import config
from ccmsproteosafepythonapi import proteosafe
from app import app

# #This displays global PCoA of public data as a web url
@app.route("/displayglobalmultivariate", methods = ["GET"])
def displayglobalmultivariate():
    return send_file("./temp/global/index.html")
    
    # if not (os.path.isfile(config.PATH_TO_ORIGINAL_PCA) and os.path.isfile(config.PATH_TO_EIGS)):
    #     print("Missing Global PCA Calculation, Calculating")
    #     if not os.path.isfile(config.PATH_TO_GLOBAL_OCCURRENCES):
    #         #Get the actual all identifictions file
    #         import urllib.request as request
    #         from contextlib import closing
    #         import shutil

    #         with closing(request.urlopen('ftp://massive.ucsd.edu/MSV000084206/other/ReDU_all_identifications.tsv')) as r:
    #             with open(config.PATH_TO_GLOBAL_OCCURRENCES, 'wb') as f:
    #                 shutil.copyfileobj(r, f)

    #     redu_pca.calculate_master_projection(config.PATH_TO_GLOBAL_OCCURRENCES)
    
    print("Begin Getting Global PCA")
    df_temp  = pd.read_csv(config.PATH_TO_ORIGINAL_PCA)
    full_file_list = df_temp["Unnamed: 0"].tolist() 
    df_temp.drop("Unnamed: 0", axis = 1, inplace = True)       
    sklearn_output = df_temp.values
        
    component_matrix = pd.read_csv(config.PATH_TO_COMPONENT_MATRIX)
    eig_var_df = pd.read_csv(config.PATH_TO_EIGS)
    eigenvalues = eig_var_df["eigenvalues"].tolist()
    percent_variance = eig_var_df["percent_variance"].tolist()

    output_file = ("./temp/global")

    redu_pca.emperor_output(sklearn_output, full_file_list, eigenvalues, percent_variance, output_file)

    return send_file("./temp/global/index.html")

# ###This takes the file selected PCA and redirects it to a new page for user viewing
# @app.route('/fileselectedpcaviews', methods=['GET'])
# def selectedpcaviews():
#     pcaid = str(request.args['pcaid'])
#     return(send_file(os.path.join('./tempuploads', pcaid, 'index.html')))

# ###This is the backend funtion for re-calcualtion of pca based on the files selected by user
# @app.route('/fileselectedpca', methods=['POST'])
# def fileselectedpca():
#     files_of_interest = json.loads(request.form["files"]) 
#     files_of_interest = [item[2:] for item in files_of_interest]
    
#     #making sure the abbreviated metadata is available
#     if os.path.isfile(config.PATH_TO_PARSED_GLOBAL_OCCURRENCES):
#         print("Parsed Global Occurrences File Found")
#         full_occ_table = pd.read_table(config.PATH_TO_PARSED_GLOBAL_OCCURRENCES) 
#         new_df = full_occ_table[full_occ_table["full_CCMS_path"].isin(files_of_interest)]       
    
#     #creating the abbreviated metadata file if not found
#     else:
#         print("Creating Parsed Global Occurrences File")
#         full_occ_table = pd.read_table(config.PATH_TO_GLOBAL_OCCURRENCES)
#         col1 = full_occ_table["full_CCMS_path"].tolist()
#         col2 = full_occ_table["Compound_Name"].tolist()
#         new_df = pd.DataFrame({"full_CCMS_path" : col1, "Compound_Name" : col2})
#         new_df.to_csv(config.PATH_TO_PARSED_GLOBAL_OCCURRENCES, sep = "\t")
#         new_df = new_df[new_df["full_CCMS_path"].isin(files_of_interest)]
         
#     sklearn_output, new_sample_list, eigenvalues, percent_variance = redu_pca.calculate_master_projection(new_df, 3, True) 
#     pcaid = str(uuid.uuid4())
#     output_folder = ("./tempuploads/" + pcaid) 
    
#     redu_pca.emperor_output(sklearn_output, new_sample_list, eigenvalues, percent_variance, output_folder)
    
#     return(pcaid) 


# @app.route('/processcomparemultivariate', methods=['GET'])
# def processcomparemultivariate():

#     knn = request.args.get("knn", "0")
#     if knn == "0":
#         nearest_neighbors = False
#     else:
#         nearest_neighbors = True

#     #Making sure we calculate global datata
#     if not os.path.isfile(config.PATH_TO_COMPONENT_MATRIX):
#         if not os.path.isfile(config.PATH_TO_GLOBAL_OCCURRENCES):
#             print("Missing Global Data")
#             return "Error", 500

#         print("Missing Global PCA Calculation, Calculating")
#         redu_pca.calculate_master_projection(config.PATH_TO_GLOBAL_OCCURRENCES)
            
#     #Making sure we grab down user query
#     task_id = request.args['task'] 
#     new_analysis_filename = os.path.join(app.config['UPLOAD_FOLDER'], task_id)
        
#     if not os.path.isfile(new_analysis_filename):
#         #TODO: Check the task type, get the URL specific for it, then reformat...
#         task_information = proteosafe.get_task_information("gnps.ucsd.edu", task_id)
#         print(task_information)

#         task_type = task_information["workflow"]

#         if task_type == "MOLECULAR-LIBRARYSEARCH-V2":
#             remote_url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&block=main&file=DB_result/".format(task_id)
#             df = pd.read_csv(remote_url, sep="\t")
#             df = df[["full_CCMS_path", "Compound_Name"]]
#             df.to_csv(new_analysis_filename, sep="\t", index=False)
#         #TODO: demangle with params filename
#         elif task_type == "METABOLOMICS-SNETS-V2":
#             clusters_url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&block=main&file=clusterinfo/".format(task_id)
#             clusters_df = pd.read_csv(clusters_url, sep="\t")

#             identifications_url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&block=main&file=result_specnets_DB/".format(task_id)
#             identifications_df = pd.read_csv(identifications_url, sep="\t")

#             inner_df = clusters_df.merge(identifications_df, how="inner", left_on="#ClusterIdx", right_on="#Scan#")
#             inner_df = inner_df[["#Filename", "Compound_Name"]]
#             inner_df["full_CCMS_path"] = inner_df["#Filename"]
#             inner_df = inner_df[["full_CCMS_path", "Compound_Name"]]

#             inner_df.to_csv(new_analysis_filename, sep="\t", index=False)
#         elif task_type == "FEATURE-BASED-MOLECULAR-NETWORKING":
#             quantification_url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&block=main&file=quantification_table_reformatted/".format(task_id)
#             quantification_df = pd.read_csv(quantification_url, sep=",")
            
#             quantification_records = quantification_df.to_dict(orient="records")

#             compound_presence_records = []
#             for record in quantification_records:
#                 for key in record:
#                     if "Peak area" in key:
#                         if record[key] > 0:
#                             presence_dict = {}
#                             presence_dict["full_CCMS_path"] = key.replace("Peak area", "")
#                             presence_dict["#ClusterIdx"] = record["row ID"]
                            
#                             compound_presence_records.append(presence_dict)
            
#             compound_presence_df = pd.DataFrame(compound_presence_records)

#             identifications_url = "https://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&block=main&file=DB_result/".format(task_id)
#             identifications_df = pd.read_csv(identifications_url, sep="\t")

#             inner_df = compound_presence_df.merge(identifications_df, how="inner", left_on="#ClusterIdx", right_on="#Scan#")
#             inner_df = inner_df[["full_CCMS_path", "Compound_Name"]]

#             inner_df.to_csv(new_analysis_filename, sep="\t", index=False)
        

#     if nearest_neighbors:
#         neighbors_list = redu_pca.project_new_data(new_analysis_filename, None, calculate_neighbors=True)
#         return render_template("multivariateneighbors.html", neighbors_list=neighbors_list)
#     else:
#         #Actually doing Analysis
#         output_folder = ("./tempuploads")
#         redu_pca.project_new_data(new_analysis_filename, output_folder)
        
#         return send_file("./tempuploads/index.html")
