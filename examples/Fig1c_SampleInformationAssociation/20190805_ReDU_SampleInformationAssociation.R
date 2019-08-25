# ReDU-MS2: Sample Information Association
# Author: Alan Jarmusch (ajarmusch@ucsd.edu)
# Date: 2019-08-12

# Load libraries
library(data.table)
library(dplyr)
library(ggplot2)
setwd("~/Research/Projects/ReDU_MS2")

# INPUT: sample information table
df <- fread("Manuscript/Data/SampleInformationAssociation/ReDU_Human_Fecal_SampleInformationAssociation_Examples.txt", sep="\t", header=TRUE, stringsAsFactors = FALSE)
dim(df)
colnames(df)

Age <- subset(df, df$Attribute == "LifeStage")

Age$Term <- factor(Age$Term, 
                   levels = c('Infancy (<2 yrs)',
                              'Early Childhood (2 yrs < x <=8 yrs)',
                              'Adolescence (8 yrs < x <= 18 yrs)',
                              'Early Adulthood (18 yrs < x <= 45 yrs)',
                              'Middle Adulthood (45 yrs < x <= 65 yrs)',
                              'Later Adulthood (>65 yrs)',
                              'not applicable', 
                              'not collected'))

Age <- subset(Age, Age$Term != "not applicable" & Age$Term != "not collected")

# PLOT: Sample Type vs. % of Files
plot <- ggplot(data=Age, aes(x= as.factor(Term), y=as.numeric(Percentage*100)))+
  facet_wrap(~Chemical, ncol=1, scale="free_y")+
  geom_bar(aes(group=Chemical), fill="grey75", stat="identity", width=0.75)+
  geom_text(aes(label=round(as.numeric(Percentage * 100),digits = 2)), size=2.5)+
  theme_minimal()+
  scale_x_discrete(labels=c("Infancy (<2 yrs)" = "Infancy", 
                            "Early Childhood (2 yrs < x <=8 yrs)" = "Early Childhood",
                            "Adolescence (8 yrs < x <= 18 yrs)" = "Adolescence",
                            "Early Adulthood (18 yrs < x <= 45 yrs)" = "Early Adulthood",
                            "Middle Adulthood (45 yrs < x <= 65 yrs)" = "Middle Adulthood",
                            "Later Adulthood (>65 yrs)" = "Later Adulthood"))+
  theme(panel.grid.major.x=element_blank(),
        panel.grid.major.y=element_line(colour="grey90",size=0.5, linetype="dashed"),
        panel.grid.minor=element_blank(),
        axis.ticks=element_line(colour ="black",size=0.5, linetype="solid"),
        axis.text=element_text(colour="black",size=6),
        axis.text.x=element_text(colour="black", size=6, angle=90),
        axis.line=element_line(colour="black",size=0.5, linetype="solid"),                  
        axis.title=element_text(colour="black",size=6),
        strip.text.x=element_text(colour="black",size=6),
        aspect.ratio=0.35,
        title=element_text(colour="black", size=6),
        legend.position="none",
        legend.title=element_text(colour="black", size=6),
        legend.text=element_text(colour="black", size=6) )+
  labs(x="", y="Annotated in Human Files (%)")
print(plot)
ggsave(plot, file="Manuscript/Figures/Source_Material/ReDU_SampleInformationAssociation.pdf", 
       width = 3.5, height = 3.5, units = "in", useDingbats=FALSE)

