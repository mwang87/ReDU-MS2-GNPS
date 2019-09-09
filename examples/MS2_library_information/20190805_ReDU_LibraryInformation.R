library(data.table)
library(dplyr)
library(ggplot2)
setwd("~/Research/Projects/ReDU_MS2")

df <- fread("Manuscript/Data/ReDU_all_identifications.tsv", sep="\t", header=TRUE)

library_GNPS <- df %>% group_by(Organism,Compound_Name) %>% summarise(Unique = n_distinct(full_CCMS_path))
library_GNPS[1:10,1:3]

library_GNPSinfo <- library_GNPS %>% group_by(Organism) %>% summarise(total_hits = sum(Unique))
colnames(library_GNPSinfo)[1] <- "library_name"

library_size <- fread("Manuscript/Data/GNPS_library_annotation_info/LIVING-DATA-SEARCH-ba6a5b6a-production_library_sizes-main.tsv", sep="\t", header=TRUE)

library_GNPSinfo_final <- library_GNPSinfo %>% left_join(library_size, by="library_name") %>% mutate(proportion = total_hits/number_spectra)

write.csv(library_GNPSinfo_final, "Manuscript/Figures/Source_Material/ReDUSummary_libraryinfo.csv", row.names=FALSE)