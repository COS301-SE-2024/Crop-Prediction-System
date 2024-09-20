library(ggplot2)

# Import data
wheat <- read.csv("wheat.csv")
corn <- read.csv("corn.csv")

# Convert timestamp to date
wheat$timestamp <- as.Date(wheat$timestamp)
corn$timestamp <- as.Date(corn$timestamp)

# Sort by date (ascending)
wheat <- wheat[order(wheat$timestamp),]
corn <- corn[order(corn$timestamp),]

# Plotting
ggplot(wheat, aes(x=timestamp, y=value)) +
  geom_line(aes(group=1)) +
  ggtitle("Wheat Prices Over Time") +
  xlab("Year") +
  ylab("Price (USD)")

ggplot(corn, aes(x=timestamp, y=value)) +
  geom_line(aes(group=1)) +
  ggtitle("Corn Prices Over Time") +
  xlab("Year") +
  ylab("Price (USD)") 
