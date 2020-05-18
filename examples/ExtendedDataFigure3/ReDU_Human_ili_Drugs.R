suppressMessages(library(data.table))
suppressMessages(library(ggplot2))
suppressMessages(library(dplyr))
suppressMessages(library(tidyr))

# import required information
df <- fread("Manuscript/Data/ReDU_all_identifications.tsv", sep="\t", header=TRUE, stringsAsFactors = FALSE)
metadata <- fread("Manuscript/Data/all_sampleinformation.tsv", sep="\t", header=TRUE, stringsAsFactors = FALSE)
metadata$filename <- sub("^f.","", metadata$filename)

drug_list <- fread("Manuscript/Data/GNPS_Curated_Source_Information_Version2.0 - Curated_Source_Information_Table (1).tsv", header=TRUE, sep="\t")

# parse all of ReDU-MS2 databased for only human files and only annotations which have been curated as drugs
human_files <- subset(metadata, metadata$NCBITaxonomy == "9606|Homo sapiens")
human_parsed_df <- df[df$full_CCMS_path %in% human_files$filename,]

drug_list <- subset(drug_list, drug_list$Source == "drug")
human_parsed_df_drugs <- human_parsed_df[human_parsed_df$Compound_Name %in% drug_list$GNPS_annotation,]

# summarize annotations by body part - collapse GNPS annotations using curated GNPS annotations
df_1 <- merge(human_parsed_df_drugs, metadata, by.x="full_CCMS_path", by.y="filename")
df_1 <- merge(df_1,drug_list, by.x="Compound_Name", by.y="GNPS_annotation")
df_1 <- table(df_1[,c("UBERONBodyPartName","Curated_GNPS_Annotation")])
df_1 <- as.data.frame.matrix(df_1)
df_1 <- cbind(rownames(df_1), df_1)
colnames(df_1)[1] <- "UBERONBodyPartName"

number_files <- metadata %>% group_by(UBERONBodyPartName) %>% tally()

df_1 <- df_1 %>% left_join(number_files, by="UBERONBodyPartName")
df_1 <- cbind(df_1[,1], sweep(df_1[,-1], df_1$n, MARGIN=1, "/"))
colnames(df_1)[1] <- "UBERONBodyPartName"

# add coordinate information by body part
coordinate_matrix <- fread("Manuscript/Data/ReDU_human_coordinates.txt", sep="\t", header=TRUE)
df_2 <- merge(coordinate_matrix, df_1, by.x="Human_Body_Part", by.y="UBERONBodyPartName")
colnames(df_2)[1] <- "filename"
write.table(df_2,"Manuscript/Data/ReDU_human_drugs.csv", sep=",", row.names=FALSE)
