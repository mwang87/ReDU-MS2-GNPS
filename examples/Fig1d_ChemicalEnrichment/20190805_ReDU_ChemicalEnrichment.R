library(data.table)
library(dplyr)
library(tidyr)
library(ggplot2)
setwd("~/Research/Projects/ReDU_MS2")

df <- fread("Manuscript/Data/ReDU_chemical_enrichment.txt", sep="\t", header=TRUE)

df[1:5,1:7]
colnames(df) <- c("Chemical",
                  "# Human Blood (n=711)","Human Blood (n=711)",
                  "# Human Urine (n=307)","Human Urine (n=307)",
                  "# Human Fecal (n=5114)","Human Fecal (n=5114)"
                  #"# of G4","Proportion of G4",
                  #"# of G5","Proportion of G5",
                  #"# of G6","Proportion of G6",
                  )

df <- df[,c(1,3,5,7)]

df_gather <- gather(data=df, sample, proportion, 2:length(df))

chemical <- "Spectral Match to Urobilin from NIST14"
#chemical <- "Bilirubin"
#chemical <- "Stercobilin"
#chemical <- "Spectral Match to L-Kynurenine from NIST14"

df_plot <- subset(df_gather, df_gather$Chemical == chemical)

plot <- ggplot(df_plot,aes(x=as.factor(sample), as.numeric(proportion*100)))+
                 geom_bar(aes(fill=sample), stat="identity", width=0.75)+
  #facet_wrap(~Comparison, ncol=3)+
  scale_fill_manual(values = c("#e41a1c","#377eb8","#fdbf6f"))+
  theme_minimal()+
  theme(panel.grid.major.x=element_blank(),
        panel.grid.major.y=element_line(colour="grey90",size=0.5, linetype="dashed"),
        panel.grid.minor=element_blank(),
        axis.ticks=element_line(colour ="black",size=0.5, linetype="solid"),
        axis.text=element_text(colour="black",size=6),
        axis.text.x=element_text(colour="black", size=6),
        axis.line=element_line(colour="black",size=0.5, linetype="solid"),                  
        axis.title=element_text(colour="black",size=6),
        strip.text.x=element_text(colour="black",size=6),
        aspect.ratio=2,
        title=element_text(colour="black", size=6),
        legend.position="none",
        legend.title=element_text(colour="black", size=6),
        legend.text=element_text(colour="black", size=6) ) +
 # labs(x="", y="Annotated in Proportion of Files", title = chemical)
  labs(x="", y="Annotated in Human Files (%)")
print(plot)  
ggsave(plot, file=paste0("Manuscript/Figures/Source_Material/ReDU_ChemicalEnrichment_",chemical,".pdf"), 
       width = 1, height = 1.15, units = "in", useDingbats=FALSE)

