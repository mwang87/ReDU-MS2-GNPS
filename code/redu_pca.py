import numpy as np
from numpy import mean
import pandas as pd
import sys
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from sklearn.decomposition import PCA

PATH_TO_COMPONENT_MATRIX = "./component_matrix.csv" #Eigenvectors
PATH_TO_ORIGINAL_PCA = "./original_pca.csv" #original PCA matrix of the original files


### Given a file input occurrence table, creates the eigen vectors file defined above PATH_TO_COMPONENT_MATRIX, and PCA project of these files PATH_TO_ORIGINAL_PCA
def calculate_master_projection(input_file_occurrences_table):
    with open(input_file_occurrences_table, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter = "\t") 
        file_list = next(reader)
    useable_cols = len(file_list)

    df = pd.read_csv(input_file_occurrences_table, sep = "\t", skip_blank_lines = True)
    compound_list = list(df["LibraryID"])

    df = pd.read_csv(input_file_occurrences_table, sep = "\t", usecols = range(2, useable_cols), header = 0, skip_blank_lines = True)

    new_matrix = df.values.transpose() #align so that the "features" are column headers

    pca = PCA(n_components = 5) #creating the instance
    pca.fit(new_matrix) #fitting the data 

    component_matrix = pca.components_ #principle components / vectors
    dataframe1 = pd.DataFrame(data = component_matrix, columns = compound_list)
    dataframe1 = dataframe1.T
    dataframe1.index.name = 'LibraryID'
    dataframe1.to_csv(PATH_TO_COMPONENT_MATRIX)

    sklearn_output = pca.transform(new_matrix) #using sklearn to calculate the output
    dataframe4 = pd.DataFrame(data = sklearn_output)
    dataframe4.index.name = "filename"
    dataframe4.to_csv(PATH_TO_ORIGINAL_PCA)


### Given a new file occurrence table, creates a projection of the new data along with the old data and saves as a png output
def project_new_data(input_file_occurrences_table, output_png):
    component_matrix = pd.read_csv(PATH_TO_COMPONENT_MATRIX, sep = ",")

    old_compound_list = list(component_matrix['LibraryID']) #list of all compounds found in the OG data

    component_matrix = component_matrix.drop(['LibraryID'], axis = 1)
    component_matrix = component_matrix.transpose()
    component_matrix.columns = old_compound_list
   
   #figuring out the filenames for the new data
    with open(PATH_TO_ORIGINAL_PCA, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter = ",") 
        file_list = next(reader)
 
        compound_location = file_list.index("filename")
        useable_cols = len(file_list)

        if compound_location == 0:
            col_range = np.arange(2, useable_cols)
        else:
            col_range = np.arange(0, useable_cols-2)

    new_compound_list = np.loadtxt(input_file_occurrences_table, dtype = str, delimiter = "\t", skiprows = 1, usecols = compound_location)
    
    new_filtered = [item for item in new_compound_list if item in old_compound_list]


    df = pd.read_csv(input_file_occurrences_table, sep = "\t", usecols = col_range, skip_blank_lines = True)
    df = df.transpose()
    df.columns = new_compound_list
    df = df[new_filtered]
    
    we_dont_care, final_matrix = component_matrix.align(df, join = 'left', axis = 1, fill_value = 0)

    final_matrix = final_matrix.values
    mean_matrix = mean(final_matrix.T, axis = 1)

    C = final_matrix - mean_matrix
    
    component_matrix = component_matrix.values.T
    we_dont_care = we_dont_care.T
      
    visualize_stuff = C.dot(we_dont_care) #manually calculating the output for projection

    
    dataframe3 = pd.DataFrame(data = visualize_stuff)
    dataframe3.to_csv("new_pca_vis.csv")
    
    omg_im_nearly_done(dataframe3, PATH_TO_ORIGINAL_PCA)

def whos_that_file(file):
    dont_care, delimiter = os.path.splitext(file)
    
    if delimiter == ".tsv":
        type = "\t"
    elif delimiter == ".csv":
        type = ","
    else:
        print("Wrong file type try again!")
        sys.exit()
    
    return(type)

def omg_im_nearly_done(new_pca_stuff, old_pca_stuff):
    typec = whos_that_file(old_pca_stuff)
    
    principal_components_new = new_pca_stuff
    principal_components_old = pd.read_csv("pca.csv", delimiter = typec)
    principal_components_old = principal_components_old.drop(['Unnamed: 0'], axis = 1)
    
    component1 = 0
    component2 = 1

    xnew = list(principal_components_new[component1])
    ynew = list(principal_components_new[component2])
    
    xold = list(principal_components_old['%s' %(component1)])
    yold = list(principal_components_old['%s' %(component2)])
   
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(xnew, ynew, s=10, c='b', marker="s", label='first')
    ax1.scatter(xold,yold, s=10, c='r', marker="o", label='second')

def main():
    input_global_file_occurrences_table = sys.argv[1]
    output_png = "output_merged_png.png"

    calculate_master_projection(input_global_file_occurrences_table)
    project_new_data(input_global_file_occurrences_table, output_png)

if __name__ == "__main__":
    main()
      