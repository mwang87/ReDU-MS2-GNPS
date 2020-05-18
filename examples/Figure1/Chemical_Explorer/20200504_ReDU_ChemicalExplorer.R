# ReDU-MS2: Chemical Explorer
# Author: Alan Jarmusch (ajarmusch@ucsd.edu)
# Date: 2020-05-04

# Load libraries
library(data.table)
library(dplyr)
library(ggplot2)
library(ggrepel)

# INPUT: sample information table
df <- fread("ReDU_Human_Fecal_ChemicalExplorer_Examples.txt", sep="\t", header=TRUE, stringsAsFactors = FALSE)
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
                              'not collected'
                              ))

Age <- subset(Age, Age$Term != "not applicable" & Age$Term != "not collected")

# PLOT: Sample Type vs. % of Files
plot <- ggplot(data=Age, aes(x= as.factor(Term), y=as.numeric(Percentage*100)))+
  facet_wrap(~Chemical, ncol=3)+
  #geom_bar(aes(group=Chemical), fill="grey75", stat="identity", width=0.75)+
  geom_text_repel(aes(label=round(as.numeric(Percentage * 100),digits = 1)), size=2.0, 
                  direction = 'y', segment.color = "blue", segment.size = 0.25)+
  geom_point(aes(group=Chemical), pch=16, cex=1.5)+
  scale_y_continuous(limits = c(0,100))+
  theme_minimal()+
  scale_x_discrete(labels=c("Later Adulthood (>65 yrs)" = "Later \n Adulthood",
                            "Middle Adulthood (45 yrs < x <= 65 yrs)" = "Middle \n Adulthood",
                            "Early Adulthood (18 yrs < x <= 45 yrs)" = "Early \n Adulthood",
                            "Adolescence (8 yrs < x <= 18 yrs)" = "Adolescence",
                            "Early Childhood (2 yrs < x <=8 yrs)" = "Early \n Childhood",
                            "Infancy (<2 yrs)" = "Infancy"))+
  theme(panel.grid.major.x=element_blank(),
        panel.grid.major.y=element_line(colour="grey90",size=0.5, linetype="dashed"),
        panel.grid.minor=element_blank(),
        axis.ticks=element_line(colour ="black",size=0.5, linetype="solid"),
        axis.text=element_text(colour="black",size=6),
        axis.text.x=element_text(colour="black", size=6, angle=90, vjust = 0.25),
        axis.line=element_line(colour="black",size=0.5, linetype="solid"),                  
        axis.title=element_text(colour="black",size=6),
        strip.text.x=element_text(colour="black",size=6),
        aspect.ratio=1.0,
        title=element_text(colour="black", size=6),
        legend.position="none",
        legend.title=element_text(colour="black", size=6),
        legend.text=element_text(colour="black", size=6) )+
  labs(x="", y="Annotated in Human Files (%)")
print(plot)
ggsave(plot, file="ReDU_ChemicalExplorer.pdf", width = 4.0, height = 3.0, units = "in", useDingbats=FALSE)

