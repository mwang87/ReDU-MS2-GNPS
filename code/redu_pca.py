import numpy as np
from numpy import mean
import pandas as pd
import sys
import os
import csv
from sklearn.decomposition import PCA
import seaborn
import matplotlib.pyplot as plt
from skbio import OrdinationResults
from emperor import Emperor
import scipy.sparse as sps

PATH_TO_COMPONENT_MATRIX = "./component_matrix.csv" #eigenvectors output by calculate_master_projection
PATH_TO_ORIGINAL_PCA = "./original_pca.csv" #original PCA matrix of the original files
PATH_TO_ORIGINAL_MAPPING_FILE = "./june11_redu_metadata.tsv" #global ReDU metadata
PATH_TO_NEW_MAPPING_FILE = "./june11_redu_metadata.tsv" #user uploaded metadata

### function takes in the condense GNPS output occurence table and reconstructs the full thing
def dense_to_sparse_matrix(input_file_occurences_table):
    #load data from master GNPS occurance table into memory
    df_temp = pd.read_csv(input_file_occurences_table, sep = "\t")
    all_compound_occurances = df_temp["Compound_Name"]
    all_file_occurances = df_temp["full_CCMS_path"]
    
    #create a new dataframe with only the information needed to reconstruct, redundant but easier to see
    compounds_filname_df = pd.DataFrame({"Compound_Name" : all_compound_occurances, "full_CCMS_path" : all_file_occurances})
    
    #sorting dataframe by sample in order to help? speed up things
    compounds_filname_df.sort_values(by = "Compound_Name", axis = 0, inplace = True)
    
    #determine the header for the new table
    unique_compounds, compound_index = np.unique(compounds_filname_df["Compound_Name"], return_inverse = True)
    
    #determine the unique samples for the new table
    unique_sample, file_index = np.unique(compounds_filname_df["full_CCMS_path"], return_inverse = True)
    
    all_compounds = list(compounds_filname_df["Compound_Name"])
    all_samples = list(compounds_filname_df["full_CCMS_path"])
    
    #create a matrix from the coordinates given
    data = [1] * len(compound_index)
    matrix = sps.coo_matrix((data, (compound_index, file_index)), shape = None).todok().toarray()
    #handling duplicates within the array
    matrix[matrix > 0] = 1
    
    #convert it into the correct format for the return
    df = pd.DataFrame(index = list(unique_compounds), columns = list(unique_sample), data = matrix)
    return(df)

### Given a file input occurrence table, creates the eigen vectors file defined above PATH_TO_COMPONENT_MATRIX, and PCA project of these files PATH_TO_ORIGINAL_PCA
def calculate_master_projection(input_file_occurrences_table, components = 5):
    #returns a sparse version of the dense input file
    sparse_occ_matrix = dense_to_sparse_matrix(input_file_occurrences_table)
    
    #separate the sparse matrix into a compound list, value matrix, and samples names
    compound_list = list(sparse_occ_matrix.index)
    sample_list = list(sparse_occ_matrix.columns)
    new_matrix = sparse_occ_matrix.values.T #align so that the "features" are column headers
    
    #format the sample list so it can be merged later with metadata
    sample_list = [("f." + item) for item in sample_list]
    
    #bring sklearn components into play
    pca = PCA(n_components = components) #creating the instance
    pca.fit(new_matrix) #fitting the data 

    eigenvalues = list(pca.explained_variance_) #eigenvalue vector                               
    percent_variance = list(pca.explained_variance_ratio_ ) #also needed for emperor percent variance explained 
    
    #calculate the component matrix and save it for projection at a later time
    component_matrix = pca.components_
    df_temp = pd.DataFrame(data = component_matrix.T, index = compound_list)
    #place eigenvalues and percent variance on the end of this file so it can be used for emperor projection
    df_temp.loc[len(compound_list)] = eigenvalues
    df_temp.loc[len(compound_list)+1] = percent_variance
    df_temp.to_csv("component_matrix.csv")
    
    sklearn_output = pca.transform(new_matrix) #using sklearn to transform the output
    
    #saving the "master pca" calculated by this function as a csv
    df_temp = pd.DataFrame(data = sklearn_output, index = sample_list)
    df_temp.to_csv("original_pca.csv")
    
    #format_for_emperor(sklearn_output, sample_list, eigenvalues, percent_variance) #TEST LINE

### Given a new file occurrence table, creates a projection of the new data along with the old data and saves as a png output
def project_new_data(new_file_occurrence_table):
    new_matrix = np.array([]) 
    file_list = []

    component_matrix = pd.read_csv(PATH_TO_COMPONENT_MATRIX, sep = ",") #read in the eigenvectors
    
    #grab the eigenvalues, percent explained variance values, and then drop them from the dataframe
    eigenvalues = list(component_matrix.iloc[-2,:])[1:]
    percent_variance = list(component_matrix.iloc[-1,:])[1:]
    component_matrix = component_matrix.iloc[:-2,:]
    
    #format eignevectors accordingly, since dataframes change when you read them is as a csv
    component_matrix.rename(columns = {'Unnamed: 0': 'SampleID'}, inplace = True)
    component_matrix.set_index(['SampleID'], inplace=True)
    
    old_compound_list = list(component_matrix.index) #list of all compounds found in the master projection and format to match

    #building the full occurance table for the new data being fed in
    new_sparse_occ_matrix = dense_to_sparse_matrix(new_file_occurrence_table)
    new_compound_list = list(new_sparse_occ_matrix.index)
    new_sample_list = list(new_sparse_occ_matrix.columns)
    
    #format new sample list ot match the metadata
    new_sample_list = ["f." + item for item in new_sample_list]

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
    #new_sample_list = [("tester" + item) for item in new_sample_list] #TEST LINE REMOVE!!!
    new_pca_df = pd.DataFrame(data = visualize_stuff, index = new_sample_list)
    new_pca_df.index.name = 'SampleID'
    new_pca_df.columns = new_pca_df.columns.astype(str)
    
    #load and format the original pca
    original_pca_df = pd.read_csv(PATH_TO_ORIGINAL_PCA, sep = ",")
    original_pca_df.rename(columns = {'Unnamed: 0': 'SampleID'}, inplace = True)
    original_pca_df.set_index(['SampleID'], inplace=True)

    all_pca_df = pd.concat([original_pca_df, new_pca_df]) #merging the two dataframes together
    
    #create things to be passed to emperor output
    values_only = all_pca_df.to_numpy()
    full_file_list = list(all_pca_df.index)
    
    #call and create an emperor output for the old data and the new projected data
    emperor_output(values_only, full_file_list, eigenvalues, percent_variance)
    

###function takes in all the calculated outputs, both sklearn and manual and places them into the ordination results formate specified by skbio and then feeds it into the emperor thing to output a plot    
def emperor_output(sklearn_output, new_files, eigenvalues, percent_variance):
    eigvals = pd.Series(data = eigenvalues)
    samples = pd.DataFrame(data = sklearn_output, index = new_files)
    p_explained = pd.Series(data = percent_variance)
    ores = OrdinationResults(long_method_name = "principal component analysis", short_method_name = "pcoa", eigvals = eigvals, samples = samples, proportion_explained = p_explained)
    
    #read in metadata files and format accordingly for emperor intake
    #this first part is for the global metadata file
    global_metadata = pd.read_csv(PATH_TO_ORIGINAL_MAPPING_FILE, sep = "\t")
    global_metadata.rename(columns = {'filename': 'SampleID'}, inplace = True)
    global_metadata["type"] = "Global Data"
    global_metadata.set_index("SampleID", inplace = True)
    
    #this part is for the user uploaded metadata file
    metadata_uploaded = pd.read_csv(PATH_TO_NEW_MAPPING_FILE, sep = "\t")
    metadata_uploaded.rename(columns = {'filename': 'SampleID'}, inplace = True)
    metadata_uploaded["type"] = "Your Data"
    change_samples = list(metadata_uploaded["SampleID"])
    #change_samples = [("tester" + item) for item in change_samples] #TEST LINE REMOVE!!!
    #metadata_uploaded["SampleID"] = change_samples #TEST LINE REMOVE!!!
    metadata_uploaded.set_index("SampleID", inplace = True)
    
    
    common = pd.concat([global_metadata, metadata_uploaded])
    #so you need to align the metadata and the files contained within the ordination file BEFORE feeding it into the Emperor thing otherwise it doesn't like to output results
    
    #making a fake dataframe on which to align things
    fake_data = np.arange(0, len(new_files))
    df_tester = pd.DataFrame(data = fake_data, index = new_files)
    
    final_metadata, unused = common.align(df_tester, join = "right", axis = 0)
    
    #call stuff to ouput an emperor plot
    emp = Emperor(ores, final_metadata)
    output_folder = 'plot' # new folder where data will be saved
    
    # create an output directory
    os.makedirs(output_folder, exist_ok=True)

    with open(os.path.join(output_folder, 'index.html'), 'w') as f:
        f.write(emp.make_emperor(standalone = True))
        emp.copy_support_files(output_folder)
    

def main():
    input_global_file_occurrences_table = sys.argv[1]
    input_new_file_occurrences_table = sys.argv[2]
    
    calculate_master_projection(input_global_file_occurrences_table)
    project_new_data(input_new_file_occurrences_table)

if __name__ == "__main__":
    main()
