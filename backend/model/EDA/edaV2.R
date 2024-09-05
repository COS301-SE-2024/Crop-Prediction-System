library(ggplot2)

# Load all the datasets
monthly <- read.csv("source/monthly.csv")
pentadal <- read.csv("source/pentadal.csv")
quarterly <- read.csv("source/quarterly.csv")
yearly <- read.csv("source/yearly.csv")

target <- read.csv("source/target.csv")

# Plot target
ggplot(target, aes(x=date, y=wheat_ton_per_hectare)) +
  geom_line(aes(group=1)) +
  ggtitle("Target") +
  labs(
    x="Date",
    y="Wheat ton per hectare",
    title="Target"
  ) +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme_minimal()