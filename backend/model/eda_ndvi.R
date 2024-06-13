library(ggplot2)
library(lubridate)
library(zoo)

# Load data
data <- read.csv("ndvi_data.csv")

# Load PET and CHIRPS data
pet_data <- read.csv("datasets/pet_data.csv")
chirps_data <- read.csv("datasets/chirps_data_interpolated.csv")

# Add PET and CHIRPS data to the NDVI data but only select as much as data allows
data$PETmean <- pet_data$mean[8:8 + nrow(data)]
data$CHIRPSmean <- chirps_data$mean[7:nrow(data)]

# Normalize CHIRPS data
data$CHIRPSmean <- (data$CHIRPSmean - min(data$CHIRPSmean)) / (max(data$CHIRPSmean) - min(data$CHIRPSmean))

data$date <- as.Date(data$date)

# Plot the data with all 3 means
ggplot(data, aes(x = date)) +
  geom_line(aes(y = PETmean, color = "Evapotranspiration (Water lost)", group = 1)) +
  geom_line(aes(y = CHIRPSmean, color = "Rainfall (Precipitation)", group = 1)) +
  geom_line(aes(y = mean, color = "Vegetation Index", group = 1)) +
  labs(title = "NDVI, PET, and CHIRPS over Time",
       x = "Date",
       y = "Value",
       color = "Legend") +
  scale_x_date(date_breaks = "1 year", date_labels = "%b %Y") +
  theme_minimal()

# Correlation between NDVI and PET
cor(data$mean, data$PETmean)

# Correlation between NDVI and CHIRPS
cor(data$mean, data$CHIRPSmean)

# Correlation between PET and CHIRPS
cor(data$PETmean, data$CHIRPSmean)
