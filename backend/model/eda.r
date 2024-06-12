library(ggplot2)
library(lubridate)

# Load data
data <- read.csv("pet_data.csv")

# Convert date column to Date type
data$date <- as.Date(data$date)

# Select data from 2019 to 2023
data_season <- data[data$date >= as.Date("2012-12-01") & data$date <= as.Date("2023-12-01"),]

# Convert date to numeric for cutting into seasons
data_season$date_numeric <- as.numeric(data_season$date - as.Date("2019-01-01"))

# Get the total season count from the dates by subtracting the first date from the last date
year_count <- (as.numeric(as.Date("2023-12-01") - as.Date("2012-12-01")) / 365)

# Make 4 times that label for each season while keeping the order
labels <- rep(c("Summer", "Autumn", "Winter", "Spring"), year_count)

# Cut the date_numeric into 4*4 intervals and label them as seasons
data_season$season <- cut(data_season$date_numeric, breaks = year_count * 4, label = labels)

# Get the mean of PET for each season
data_stats <- aggregate(data_season$mean, by=list(data_season$season), FUN=mean)

# Plot the means of PET for each season
ggplot(data_stats, aes(x=Group.1, y=x, fill=Group.1)) +
  geom_bar(stat="identity") +
  labs(title="Means of PET by Season",
       x="Season",
       y="Mean") +
  theme_minimal()

# Plot the data highlighting the seasons with the same color
ggplot(data_season, aes(x=date, y=mean, color=season)) +
  geom_point() +
  labs(title="Means of PET Over Time",
       x="Date",
       y="Mean") +
  theme_minimal()

# Plot a regression line for the data
ggplot(data_season, aes(x=date, y=mean, color=season)) +
  geom_point() +
  labs(title="Means of PET Over Time with Regression Line",
       x="Date",
       y="Mean") +
  theme_minimal()

# Prepare the data for a boxplot
data_season$season <- factor(data_season$season, levels=c("Summer", "Autumn", "Winter", "Spring"))

# Plot a boxplot of the data
ggplot(data_season, aes(x=season, y=mean, fill=season)) +
  geom_boxplot() +
  labs(title="Boxplot of PET by Season",
       x="Season",
       y="Mean") +
  theme_minimal()

  
