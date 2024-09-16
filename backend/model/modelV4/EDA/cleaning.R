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
HD <- read.csv("historical_data_cleaned.csv")

# [1] "name"             "datetime"         "tempmax"          "tempmin"          "temp"             "feelslikemax"    
# [7] "feelslikemin"     "feelslike"        "dew"              "humidity"         "precip"           "precipprob"      
# [13] "precipcover"      "preciptype"       "snow"             "snowdepth"        "windgust"         "windspeed"       
# [19] "winddir"          "sealevelpressure" "cloudcover"       "visibility"       "solarradiation"   "solarenergy"     
# [25] "uvindex"          "severerisk"       "sunrise"          "sunset"           "moonphase"        "conditions"      
# [31] "description"      "icon"             "stations"      

# data <- HD %>%
  # select(-c("name", "temp", "feelslikemax", "feelslikemin", "feelslike", "precipcover", "preciptype", "snowdepth", "windgust", "winddir", "severerisk", "sunrise", "sunset", "moonphase", "conditions", "description", "icon", "stations", "snow", "windspeed", "visibility"))

# Feature engineering
# data$date <- as.Date(data$datetime)

# Drop date column
# data <- data %>%
#   select(-datetime)
# 
# # Make date the first column
# data <- data %>%
#   select(date, everything())

# Rename colnames to match OpenWeather API
# names(data)[names(data) == "dew"] <- "dew_point"
# names(data)[names(data) == "precip"] <- "rain"
# names(data)[names(data) == "cloudcover"] <- "clouds"
# names(data)[names(data) == "uvindex"] <- "uvi"
# names(data)[names(data) == "precipprob"] <- "pop"
# names(data)[names(data) == "sealevelpressure"] <- "pressure"

# data$tempmean <- (data$tempmax + data$tempmin) / 2
# data$tempdiurnal <- data$tempmax - data$tempmin

# Plot all variables with date as x-axis
# data %>%
#   gather(-date, key = "some_var_name", value = "some_value_name") %>%
#   ggplot(aes(x = some_value_name, y = date, color = some_var_name)) +
#   geom_point() +
#   facet_wrap(~ some_var_name, scales = "free") +
#   labs(
#     x = "Value",
#     y = "Date",
#     title = "Historical Weather data in Pretoria",
#     fill = "Variable"
#   ) +
#   theme(
#     plot.title = element_text(hjust = 0.5),
#     axis.text.x = element_text(angle = 45, hjust = 1)
#   ) +
#   theme_minimal()

# Show missing values
vis_miss(HD)

# Convert individual NA values to NULL
data[is.na(data)] <- ""

# Save as csv
# write.csv(data, "historical_data_cleaned.csv", row.names = FALSE)


