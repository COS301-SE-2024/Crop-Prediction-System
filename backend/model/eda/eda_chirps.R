library(ggplot2)
library(lubridate)
library(zoo)
library(dplyr)

# Load data
data <- read.csv("chirps_data.csv")
data_v2 <- read.csv("chirps_data_v2.csv")

# Merge the two datasets
data <- rbind(data, data_v2)

# Convert date column to Date type
data$date <- as.Date(data$date)

# Select data from 2012 onwards
data_season <- data[data$date >= as.Date("2012-01-01"),]

# Interpolate data to increase density (daily frequency)
full_dates <- seq(min(data_season$date), max(data_season$date), by = "day")
interpolated_data <- data.frame(date = full_dates)

# Use linear interpolation for the 'mean' column
interpolated_data$mean <- approx(data_season$date, data_season$mean, xout = full_dates)$y

# Add other columns with linear interpolation
interpolated_data$stdev <- approx(data_season$date, data_season$stdev, xout = full_dates)$y
interpolated_data$var <- approx(data_season$date, data_season$var, xout = full_dates)$y
interpolated_data$median <- approx(data_season$date, data_season$median, xout = full_dates)$y
interpolated_data$iqr <- approx(data_season$date, data_season$iqr, xout = full_dates)$y

# Calculate a moving average with a window of 30 days
interpolated_data$mean <- rollmean(interpolated_data$mean, k = 5, fill = NA, align = "center")
interpolated_data$stdev <- rollmean(interpolated_data$stdev, k = 5, fill = NA, align = "center")
interpolated_data$var <- rollmean(interpolated_data$var, k = 5, fill = NA, align = "center")
interpolated_data$median <- rollmean(interpolated_data$median, k = 5, fill = NA, align = "center")
interpolated_data$iqr <- rollmean(interpolated_data$iqr, k = 5, fill = NA, align = "center")

# Select every 5th day for better visualization
interpolated_data <- interpolated_data[seq(1, nrow(interpolated_data), by = 5),]

# Discard the first and last rows with NA values
interpolated_data <- interpolated_data[complete.cases(interpolated_data),]

# Plot the smoothed data
ggplot(interpolated_data, aes(x = date, y = mean)) +
  geom_line() +
  labs(title = "Smoothed Means of CHIRPS Over Time",
       x = "Date",
       y = "Mean (Smoothed)") +
  theme_minimal()

# Save the interpolated and smoothed data to a new CSV file
write.csv(interpolated_data, "chirps_data_interpolated.csv", row.names = FALSE)
