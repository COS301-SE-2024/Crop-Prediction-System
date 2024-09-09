# Call an API to get the data
# The API is from https://api.terrabyte.software/getTeamFieldData?team_id=17383e3d-f211-4724-8515-8c4cb836c812

library(jsonlite)
library(dplyr)
library(ggplot2)
library(zoo)

data <- fromJSON("https://api.terrabyte.software/getTeamFieldData?team_id=17383e3d-f211-4724-8515-8c4cb836c812")

data <- data %>%
  select(date, yield) %>%
  group_by(date) %>%
  summarise(yield = mean(yield))

# Remove last row
data <- data[-nrow(data), ]

# Calculate rolling mean
data$rolling_mean <- rollmean(data$yield, 7, na.pad=TRUE)

# Convert date to Date object
data$date <- as.Date(data$date)

# Plot the data
ggplot(data, aes(date, yield)) +
  geom_line(aes(group = 1), color = "gray") +
  geom_line(aes(y = rolling_mean, group = 1), color = "red") +
  geom_vline(xintercept = as.numeric(as.Date("2024-08-31")), linetype = "solid", color = "blue", size = 1.5) +
  labs(title = "Yield over time",
       x = "Date",
       y = "Yield") +
  theme_bw()
