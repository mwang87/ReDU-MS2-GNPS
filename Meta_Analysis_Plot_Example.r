


library(ggplot2)
library(tidyr)

args <- commandArgs(trailingOnly=TRUE)
user_input <- args[4]

df <- read.delim(args[1], sep="\t", header =TRUE)
df <- separate(data = df,col = source.information, into = c("source_level", "category"), sep = "_")
df3 <- gather(df, group, number, G1.number, G2.number, G3.number,factor_key=TRUE)
df2 <- gather(df, group, percent, G1.percent, G2.percent, G3.percent,factor_key=TRUE)
df3 <- separate(data = df3, col = group, into = c("group","disregard"))
df2 <- separate(data = df2, col = group, into = c("group","disregard"))


gg_bar_number <- ggplot(subset(df3,df3$source_level == user_input), aes(x=reorder(category, -number), y = number, fill=group))+
    geom_bar(stat = "identity", width= 0.75, position = position_dodge(width=0.75))+
    scale_fill_brewer(palette = "Set1")+
    scale_y_continuous(limits=c(0,max(df3$number)+1000))+
    geom_text(aes(label=number), position = position_dodge(width=0.75), vjust=0.25, hjust=-0.5, size=2) +
            theme(panel.background = element_rect(fill="white"),
                  panel.grid.major=element_blank(),
                  panel.grid.minor=element_blank(),
                  axis.ticks=element_line(colour ="black",size=0.5, linetype="solid"),
                  axis.text=element_text(size=8),
                  axis.text.x=element_text(angle=0, hjust=0.5, vjust=1.25),
                  axis.line=element_line(colour="black",size=0.5, linetype="solid"),
                  axis.title=element_text(size=8),
                  aspect.ratio=1,
                  legend.position="bottom",
                  legend.title=element_blank(),
                  legend.text=element_text(size=6))
gg_bar_number <- gg_bar_number +  labs(x="Category", y="Number of Files") +  coord_flip()
print(gg_bar_number)
ggsave(args[2], device = "png", width=5, height=5,unit="in", dpi = 120)

gg_bar_percent <- ggplot(subset(df2,df2$source_level == user_input), aes(x=reorder(category, -percent), y = percent, fill=group))+
    geom_bar(stat = "identity", width= 0.75, position = position_dodge(width=0.75))+
    scale_fill_brewer(palette = "Set1")+
    scale_y_continuous(limits=c(0,100))+
    geom_text(aes(label=percent), position = position_dodge(width=0.75), vjust=0.25, hjust=-0.5, size=2) +
            theme(panel.background = element_rect(fill="white"),
                  panel.grid.major=element_blank(),
                  panel.grid.minor=element_blank(),
                  axis.ticks=element_line(colour ="black",size=0.5, linetype="solid"),
                  axis.text=element_text(size=8),
                  axis.text.x=element_text(angle=0, hjust=0.5, vjust=1.25),
                  axis.line=element_line(colour="black",size=0.5, linetype="solid"),
                  axis.title=element_text(size=8),
                  aspect.ratio=1,
                  legend.position="bottom",
                  legend.title=element_blank(),
                  legend.text=element_text(size=6))
gg_bar_percent <- gg_bar_percent +  labs(x="Category", y="Percent of Files (%)") +  coord_flip()
print(gg_bar_percent)
print(args[3])
ggsave(args[3], device = "png", width=5, height=5,unit="in", dpi = 120)
