import numpy as np
from numpy import mean
import pandas as pd
import sys
import os
import csv 
import seaborn
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from skbio.stats.ordination import OrdinationResults
from emperor import Emperor
import scipy.sparse as sps
import config
from numpy import genfromtxt
import collections
import scipy

### Given a file input occurrence table, creates the eigen vectors file defined above PATH_TO_COMPONENT_MATRIX, and PCA project of these files PATH_TO_ORIGINAL_PCA
def calculate_master_projection(input_file_occurrences_table, components = 3, smol_pca = False):  
    print("Calulating Master Projection")
    #determine whether or not this is a full calculation
    if smol_pca is False:
        #load data from master GNPS occurance table into memory
        df_temp = pd.read_table(input_file_occurrences_table)    
    else:
        #whole table has already been passed
        df_temp = input_file_occurrences_table
    print(df_temp)
    #reading in filenames and compound names
    all_compound_occurances = df_temp["Compound_Name"]
    all_file_occurances = df_temp["full_CCMS_path"]  
    
    #determine the header for the new table
    unique_compounds, compound_index = np.unique(all_compound_occurances, return_inverse = True)
    
    #determine the unique samples for the new table
    unique_sample, file_index = np.unique(all_file_occurances, return_inverse = True)
    
    #create a matrix from the coordinates given
    data = [1] * len(compound_index)
    matrix = sps.coo_matrix((data, (compound_index, file_index)), shape = None).todok().toarray()
    
    #handling duplicates within the array
    matrix[matrix > 0] = 1
    
    #convert it into the correct format for the return
    sparse_occ_matrix = pd.DataFrame(index = list(unique_compounds), columns = list(unique_sample), data = matrix)
    new_matrix = sparse_occ_matrix.T.values #align so that the "features" are column headers
    
    #bring sklearn components into play
    pca = PCA(n_components = components, copy = False) #creating the instance
    sklearn_output = pca.fit_transform(new_matrix) #fitting the data 
    
    eigenvalues = list(pca.explained_variance_) #eigenvalue vector
    percent_variance = list(pca.explained_variance_ratio_ ) #also needed for emperor percent variance explained
   
    print("GLOBAL")
    unique_sample = ["f." + item for item in unique_sample]
    if smol_pca is False:
        #calculate the component matrix and save it for projection at a later time
        component_matrix = pca.components_
        component_df = pd.DataFrame(data = component_matrix.T, index = unique_compounds)
        component_df.to_csv(config.PATH_TO_COMPONENT_MATRIX)

        #save eigenvalues and percent variance for later
        df_temp = pd.DataFrame({"eigenvalues" : eigenvalues, "percent_variance" : percent_variance})
        df_temp.to_csv(config.PATH_TO_EIGS)
        
        #save principle components for later
        df_temp = pd.DataFrame(data = sklearn_output, index = unique_sample)
        df_temp.to_csv(config.PATH_TO_ORIGINAL_PCA)

    if smol_pca is True:
        return(sklearn_output, unique_sample, eigenvalues, percent_variance)    

### Given a new file occurrence table, creates a projection of the new data along with the old data and saves as a png output
def project_new_data(new_file_occurrence_table, output_file, calculate_neighbors=False):
    new_matrix = np.array([]) 
    file_list = []
    
    #load components, eigenvalues, and percent variance
    component_matrix = pd.read_csv(config.PATH_TO_COMPONENT_MATRIX, sep = ",")
    eig_var_df = pd.read_csv(config.PATH_TO_EIGS, sep = ",")
    eigenvalues = eig_var_df["eigenvalues"].tolist()
    percent_variance = eig_var_df["percent_variance"].tolist()
   
    #format eignevectors accordingly, since dataframes change when you read them is as a csv
    component_matrix.rename(columns = {'Unnamed: 0': 'SampleID'}, inplace = True)
    component_matrix.set_index(['SampleID'], inplace=True)
    
    old_compound_list = list(component_matrix.index) #list of all compounds found in the master projection and format to match

    #reformat the occurance table for the new data being fed in
    new_data = pd.read_table(new_file_occurrence_table)
    all_compound_occurances = new_data["Compound_Name"]
    all_file_occurances = new_data["full_CCMS_path"]
     
    #sorting dataframe by sample in order to help? speed up things
    new_data.sort_values(by = "Compound_Name", axis = 0, inplace = True)
    
    #determine the header for the new table
    unique_compounds, compound_index = np.unique(new_data["Compound_Name"], return_inverse = True)
    
    #determine the unique samples for the new table
    unique_sample, file_index = np.unique(new_data["full_CCMS_path"], return_inverse = True)
    
    all_compounds = list(new_data["Compound_Name"])
    all_samples = list(new_data["full_CCMS_path"])
    
    #create a matrix from the coordinates given
    data = [1] * len(compound_index)
    
    matrix = sps.coo_matrix((data, (compound_index, file_index)), shape = None).todok().toarray()
    #handling duplicates within the array
    matrix[matrix > 0] = 1
    
    #convert it into the correct format for the return
    new_sparse_occ_matrix = pd.DataFrame(index = list(unique_compounds), columns = list(unique_sample), data = matrix)

    new_compound_list = list(unique_compounds)        
    new_sample_list = list(unique_sample)    	     	
    #determine which compounds are common between the original and new datasets
    find_common_compounds = [item for item in new_compound_list if item in old_compound_list]

    #remove compounds that are not a part of the original matrix, un-calculted compound occurances cannot be compared via projection
    new_sparse_occ_matrix = new_sparse_occ_matrix.T #flip so we can filter by columns
    new_sparse_occ_matrix = new_sparse_occ_matrix[find_common_compounds]
    new_sparse_occ_matrix = new_sparse_occ_matrix.T #reflip so compounds are row for alignment reasons
    
    #align orignal pca eigenvalues and new occurance table such that the correct compounds will be multiplied against each other and the projection will be correct
    components, new_matrix = component_matrix.align(new_sparse_occ_matrix, join = "left", axis = 0, fill_value = 0)   
    #removing all compound names and sampleIDs for matrix multiplcation, manually calcuating projection output 
    final_matrix = new_matrix.values.T
    mean_matrix = mean(final_matrix.T, axis = 1) #matrix gets transformed in this line
    C = final_matrix - mean_matrix

    components = components.values #transforming components for multiplcation
      
    visualize_stuff = C.dot(components) #manually calculating the output for projection
    
    #format new projection into a dataframe 
    new_pca_df = pd.DataFrame(data = visualize_stuff, index = new_sample_list)
    new_pca_df.index.name = 'Unnamed: 0'
    new_pca_df.columns = new_pca_df.columns.astype(str)

    #load and format the original pca
    original_pca_df = pd.read_csv(config.PATH_TO_ORIGINAL_PCA, sep = ",")
    original_pca_df.set_index(['Unnamed: 0'], inplace=True) 
    if calculate_neighbors:
        all_neighbors = [] 
        ary = scipy.spatial.distance.cdist(new_pca_df, original_pca_df, metric='euclidean')    
       
        for i in range(len(ary)):
            neighbor_distances_df = pd.DataFrame()            
            neighbor_distances_df["filename"] = original_pca_df.index
            neighbor_distances_df["distance"] = ary[i,:]
            neighbor_distances_df = neighbor_distances_df.sort_values("distance")
            df = pd.read_table(config.PATH_TO_ORIGINAL_MAPPING_FILE)
            neighbor_distances_df = neighbor_distances_df.merge(df, how="left", left_on="filename", right_on="filename")
            neighbor_distances_df["query"] = new_pca_df.index[i]

            all_neighbors += neighbor_distances_df.to_dict(orient="records")[:100]
              
        return(all_neighbors)
    
    all_pca_df = pd.concat([original_pca_df, new_pca_df]) #merging the two dataframes together
    
    #create things to be passed to emperor output
    values_only = all_pca_df.to_numpy()
    full_file_list = list(all_pca_df.index) 
    
    #call and create an emperor output for the old data and the new projected data
    emperor_output(values_only, full_file_list, eigenvalues, percent_variance, output_file, new_sample_list)
    
  
###function takes in all the calculated outputs and places them into the ordination results and then feeds it into the emperor thing to output a plot   
def emperor_output(sklearn_output, full_file_list, eigenvalues, percent_variance, output_file, new_files = []):   
    eigvals = pd.Series(data = eigenvalues)
    samples = pd.DataFrame(data = sklearn_output, index = full_file_list)
    samples.index.rename("SampleID", inplace = True)
    p_explained = pd.Series(data = percent_variance)
    ores = OrdinationResults(long_method_name = "principal component analysis", short_method_name = "pcoa", eigvals = eigvals, samples = samples, proportion_explained = p_explained)
     
    #read in all sample metadata 
    df = pd.read_table(config.PATH_TO_ORIGINAL_MAPPING_FILE)
    df.rename(columns={"filename" : "SampleID"}, inplace = True)
    df.set_index("SampleID", inplace = True)
    
    #handling the case in which the pca is a projection
    if len(new_files) != 0:
        df["Type"] =  "Global"
        new_meta = pd.DataFrame({"SampleID" : new_files, "Type": "Your Data"})
        new_meta.set_index("SampleID", inplace = True)
        df = pd.concat([df, new_meta], axis = 0, join = "outer")
      
    final_metadata, unused = df.align(samples,join = "right", axis = 0)    
    
    #call stuff to ouput an emperor plot
    emp = Emperor(ores, final_metadata , remote = True)
               
    # create an output directory
    os.makedirs(output_file, exist_ok=True)
    
    with open(os.path.join(output_file, 'index.html'), 'w') as f:
        f.write(emp.make_emperor(standalone = True))
        emp.copy_support_files(output_file)


