suppressMessages(library(data.table))
suppressMessages(library(ggplot2))
suppressMessages(library(dplyr))
suppressMessages(library(tidyr))
library(ggmap)
#library(maptools)
library(maps)
library(viridis)


# import required information
df <- fread("Manuscript/Data/ReDU_all_identifications.tsv", sep="\t", header=TRUE, stringsAsFactors = FALSE)
metadata <- fread("Manuscript/Data/all_sampleinformation_latlongcleaned.txt", sep="\t", header=TRUE, stringsAsFactors = FALSE)
metadata$filename <- sub("^f.","", metadata$filename)

df_1 <- merge(metadata, df, by.x="filename", by.y="full_CCMS_path")


number_files <- df_1 %>% group_by(LatitudeandLongitude, Lat, Long) %>% summarise(Unique = n_distinct(filename))
chemical_sum <- df_1 %>% group_by(LatitudeandLongitude, Lat, Long, Compound_Name) %>% summarise(Files = n_distinct(filename)) 
chemical_sum <- chemical_sum %>% group_by(LatitudeandLongitude, Lat, Long) %>% summarise(total_hits = sum(Files))
plot_sum <- chemical_sum %>% left_join(number_files[,c("LatitudeandLongitude","Unique")], by="LatitudeandLongitude") %>% mutate(proportion = total_hits/Unique)



### PLOT NUMBER OF FILES
plot_number_files <- subset(number_files, number_files$Lat != "not specified" & number_files$Lat != "not applicable")
plot_number_files$Unique <- log(plot_number_files$Unique,10)
#Using GGPLOT, plot the Base World Map
mp <- NULL
mapWorld <- borders("world", colour="gray90", fill="gray90") # create a layer of borders
mp <- ggplot() +  mapWorld 
print(mp)
#Now Layer the cities on top
mp <- mp + geom_point(data=plot_number_files, aes(x=as.numeric(Long), y=as.numeric(Lat), colour=as.numeric(Unique)), size=1.5, alpha=0.7) +
  scale_color_viridis(option="B")+
  theme_minimal()+
  theme(legend.position="bottom",
        legend.title=element_text(colour="black", size=6),
        legend.text=element_text(colour="black", size=6))+
  labs(x="Longitude", y="Latitude", colour = "Log10(# of Files)")
print(mp)
#ggsave(mp, file="Manuscript/Figures/Source_Material/ReDU_Map_NumberofFiles.pdf", width = 8, height = 5, units = "in", useDingbats=FALSE)


### PLOT NUMBER OF ANNOTATIONS / FILE
plot_sum <- subset(plot_sum, plot_sum$Lat != "not specified" & plot_sum$Lat != "not applicable")
plot_sum$proportion <- log(plot_sum$proportion,10)
#Using GGPLOT, plot the Base World Map
mp <- NULL
mapWorld <- borders("world", colour="gray90", fill="gray90", size=0.25) # create a layer of borders
mp <- ggplot() +  mapWorld 
#Now Layer the cities on top
mp <- mp + geom_point(data=plot_sum, aes(x=as.numeric(Long), y=as.numeric(Lat), colour=as.numeric(proportion)), 
                      pch=16, size=0.5, alpha=0.7) +
  scale_color_viridis(option="B")+
  theme_minimal()+
  theme(axis.ticks=element_line(colour ="black",size=0.5, linetype="solid"),
        axis.text=element_text(colour="black",size=6),
        axis.title=element_text(colour="black",size=6),
        axis.line=element_line(colour="black",size=0.5, linetype="solid"),                  
        legend.position="bottom",
        legend.title=element_text(colour="black", size=6),
        legend.text=element_text(colour="black", size=6))+
  labs(x="Longitude", y="Latitude", colour = "Log10(# of Annotations / # of Files)")
print(mp)
ggsave(mp, file="Manuscript/Figures/Source_Material/ReDU_Map_NumberofAnnotationsPerFile.pdf", 
       width = 3.5, height = 2.5, units = "in", useDingbats=FALSE)






### PLOT SPECIFIC CHEMICAL

chemical_to_plot <- "Spectral Match to Tris(2-butoxyethyl) phosphate from NIST14"

plot <- subset(df_1,df_1$Compound_Name == chemical_to_plot)

#Using GGPLOT, plot the Base World Map
mp <- NULL
mapWorld <- borders("world", colour="gray50", fill="gray50") # create a layer of borders
mp <- ggplot() +  mapWorld 
print(mp)
#Now Layer the cities on top
mp <- mp + geom_point(data=plot, aes(x=as.numeric(Long), y=as.numeric(Lat)), size=3) 
print(mp)








