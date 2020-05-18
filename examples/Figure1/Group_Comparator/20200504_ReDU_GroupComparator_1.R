# ReDU-MS2: Group Comparator
# Author: Alan Jarmusch (ajarmusch@ucsd.edu)
# Date: 2020-05-04

library(data.table)
library(dplyr)
library(tidyr)
library(ggplot2)
library(ggrepel)

df <- fread("20200504_ReDU_GroupComparator_1.csv", sep=",", header=TRUE)

df <- df %>% select(Compound, 8:13)

colnames(df) <- c("Chemical",
                  "Human Blood \n (n = 711)",
                  "Human Fecal \n (n = 5097)",
                  "Human Urine \n (n = 307)",
                  "# of G4",
                  "# of G5",
                  "# of G6")

evalute_if_can_drop <- df[,apply(df,2,function(x) !all(x==0))]

df <- df[,-c(5:7)]

chemicals_to_plot <- c("Bilirubin", "Spectral Match to Urobilin from NIST14","Stercobilin")

df_chemicals_to_plot <- df[df$Chemical %in% chemicals_to_plot,]

df_plot <- gather(data=df_chemicals_to_plot, sample, percentage, 2:length(df))

plot <- ggplot(data=df_plot, aes(x= as.factor(sample), y=as.numeric(percentage)))+
  facet_wrap(~Chemical, ncol=3)+
  #geom_bar(aes(group=Chemical), fill="grey75", stat="identity", width=0.75)+
  geom_text_repel(aes(label=round(as.numeric(percentage),digits = 1)), size=2.0, 
                  direction = 'y', segment.color = "blue", segment.size = 0.25)+
  geom_point(aes(group=Chemical), pch=16, cex=1.5)+
  #coord_flip()+
  scale_y_continuous(limits = c(0,100))+
  theme_minimal()+
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
ggsave(plot, file="ReDU_GroupComparator_Human.pdf", width = 4.0, height = 3.0, units = "in", useDingbats=FALSE)

