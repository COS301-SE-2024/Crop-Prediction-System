library(ggplot2)
library(zoo)
library(corrplot)
library(reshape2)
library(dplyr)
library(tensorflow)
library(keras)
library(GGally)
library(tidyr)

# Load all the datasets
OW <- read.csv("OW_bulk.csv")
HD <- read.csv("historical_data.csv")

# colnames(OW)
# [1] "dt"                  "dt_iso"              "timezone"            "city_name"           "lat"                
# [6] "lon"                 "temp"                "visibility"          "dew_point"           "feels_like"         
# [11] "temp_min"            "temp_max"            "pressure"            "sea_level"           "grnd_level"         
# [16] "humidity"            "wind_speed"          "wind_deg"            "wind_gust"           "rain_1h"            
# [21] "rain_3h"             "snow_1h"             "snow_3h"             "clouds_all"          "weather_id"         
# [26] "weather_main"        "weather_description" "weather_icon"

data <- OW %>%
  select(-c("dt", "visibility", "timezone", "city_name", "lat", "lon", "weather_id", "weather_main", "weather_description", "weather_icon", "temp", "feels_like", "sea_level", "grnd_level", "wind_gust", "wind_deg", "wind_speed", "rain_3h", "snow_1h", "snow_3h"))

# Convert dt_iso to date
data$dt_iso <- as.Date(data$dt_iso)

# Fill NA values with 0
data[is.na(data)] <- 0

# Aggregate data by day (some sum others mean)
data <- data %>%
  group_by(dt_iso) %>%
  summarise(across(c(pressure, humidity, clouds_all, dew_point), mean), across(c(rain_1h), sum), across(c(temp_max), max), across(c(temp_min), min))

# Create a new column with tempmean and temp diurnal
data$tempmean <- (data$temp_min + data$temp_max) / 2
data$tempdiurnal <- data$temp_max - data$temp_min

# Rename columns to match the names:
# date,tempmax,tempmin,dew_point,humidity,rain,pop,pressure,clouds,solarradiation,solarenergy,uvi,tempmean,tempdiurnal
colnames(data) <- c("date", "pressure", "humidity", "clouds", "dew_point", "rain", "tempmax", "tempmin", "tempmean", "tempdiurnal")

# Convert HD's date to date
HD$date <- as.Date(HD$date)

# Select data from HD where the date is in the range of the data from OW
HD <- HD %>%
  select(date, solarradiation, solarenergy, uvindex) %>%
  filter(date >= min(data$date) & date <= max(data$date))

# Merge both datasets
data <- merge(data, HD, by = "date", all.x = TRUE)

names(data)[names(data) == "uvindex"] <- "uvi"

# Export as CSV
write.csv(data, "cleaned_data.csv", row.names = FALSE)

