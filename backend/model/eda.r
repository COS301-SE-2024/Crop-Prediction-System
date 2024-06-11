# ggplot
library(ggplot2)

# load data
data <- read.csv("ndvi_local_all.csv")

# plot mean_normalized_ndvi from data with error bars and y axis date and x axis mean_normalized_ndvi
# geom_path: Each group consists of only one observation. Do you need to adjust the group aesthetic?
ggplot(data, aes(x=date, y=mean_normalized_ndvi, group=1)) +
  geom_point() +
  geom_path() +
  theme_minimal() +
  labs(title="Mean Normalized NDVI with Error Bars", x="Date", y="Mean Normalized NDVI") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))