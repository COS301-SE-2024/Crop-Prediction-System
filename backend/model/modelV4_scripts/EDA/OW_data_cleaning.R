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
OW <- read.csv("field_data_rows.csv")

# [1] "field_id"         "date"             "summary"          "tempmax"         
# [5] "tempmin"          "tempdiurnal"      "tempmean"         "pressure"        
# [9] "humidity"         "dew_point"        "clouds"           "pop"             
# [13] "rain"             "uvi"              "gff"              "gdd"             
# [17] "hdd"              "soil_moisture"    "soil_temperature" "pet"             
# [21] "health"           "yield"            "sprayability" 
# Drop wind_ columns
OW <- OW %>%
  select(-c("wind_speed", "wind_deg", "wind_gust", "pop", "gff", "gdd", "hdd", "pet"))

# Rename health to pred_health
colnames(OW)[colnames(OW) == "health"] <- "pred_health"

# Rename sprayability to pred_sprayability
colnames(OW)[colnames(OW) == "sprayability"] <- "pred_sprayability"

# Rename yield to pred_yield
colnames(OW)[colnames(OW) == "yield"] <- "pred_yield"

# Clear soil_moisture and soil_temperature to null
OW$soil_moisture <- 0
OW$soil_temperature <- 0

# Replace NA with 0
OW[is.na(OW)] <- 0

# Save as CSV
write.csv(OW, "cleaned_field_data.csv", row.names = FALSE)


