# This file is to build the training and testing data, export it to a csv file, to be analyzed and trained in Python.
library(dplyr)
library(tidyr)
library(corrplot)

# Import the data
data <- read.csv("./processed_data/uea_converted.csv") # monthly
satellite_data <- read.csv("./processed_data/combined_data.csv") # pentadal
gdd <- read.csv("./processed_data/growing_season.csv") # yearly
yield <- read.csv("./processed_data/yield.csv") # yearly
soil <- read.csv("./processed_data/soil.csv") # yearly

# Convert the date to year in the format 01-JAN-1902
soil$Year <- as.Date(paste0("01-JAN-", soil$Year), format = "%d-%b-%Y")

# Add prefix to soil columns
soil <- soil %>% rename_with(~paste0("soil_", .), -Year)

# Convert the date to year in the format 01-JAN-1902
data$date <- as.Date(data$date, format = "%d-%b-%Y")

# Convert 2012-02-10 to date
satellite_data$date <- as.Date(satellite_data$date)

# Add prefix to satellite_data columns
satellite_data <- satellite_data %>% rename_with(~paste0("satellite_", .), -date)

gdd$date <- as.Date(paste0("01-JUL-", gdd$year), format = "%d-%b-%Y")

# Convert 1910/11 to 1910
yield$production_year <- as.numeric(substr(yield$production_year, 1, 4))
yield$harvest_date <- as.Date(paste0("01-MAR-", yield$production_year+1), format = "%d-%b-%Y")

# Put harvest_date first
yield <- yield %>% select(harvest_date, everything())

# Remove production_year in yield
yield <- yield %>% select(-production_year)

# Make date column first and remove year column in gdd
gdd <- gdd %>% select(date, gdd)

# Merge data with gdd
result <- merge(data, gdd, by = "date", all.x = TRUE)

# With yield, remove all columns that end with "ton_per_hectare"
# yield <- yield %>% select(-contains("ton_per_hectare"))

# With yield, select harvest_date and all columns that end with "ton_per_hectare"
yield <- yield %>% select(harvest_date, contains("ton_per_hectare"))

# Remove column named X in yield
# yield <- yield %>% select(-X)

# Merge result with yield
# result <- result %>% full_join(yield, by = c("date" = "harvest_date"))
result <- merge(result, yield, by.x = "date", by.y = "harvest_date", all.x = TRUE)

# Merge result with soil
result <- result %>% left_join(soil, by = c("date" = "Year"))

# Calculate monthly average of all columns in satellite_data
# Get distinct year and month
satellite_data$year_month <- format(satellite_data$date, "%b-%Y")

# Get the average of all columns in satellite_data
satellite_data <- satellite_data %>% group_by(year_month) %>% summarise_all(mean)

# Remove date and csi column in satellite_data
satellite_data <- satellite_data %>% select(-date, -satellite_CSI)

# Convert the date (2012-02) to year in the format 01-JAN-1902
satellite_data$date <- as.Date(paste0("01-", satellite_data$year_month), format = "%d-%b-%Y")

# Remove year_month in satellite_data
satellite_data <- satellite_data %>% select(-year_month)

# Full join result with satellite_data
# result <- result %>% full_join(satellite_data, by = c("date" = "date"))
result <- merge(result, satellite_data, by = "date", all.x = TRUE)

# Forward-fill the "ton_per_hectare" columns for 11 months
result <- result %>% fill(contains("ton_per_hectare"), .direction = "up")
# 
# # Forward-fill the "soil_" columns for 11 months
result <- result %>% fill(starts_with("soil_"), .direction = "up")

# Calculate TempScore


# Add complete columns
res <- complete(result, date = seq.Date(min(result$date), max(result$date), by = "month"))

# Sort the data by date
result <- result[order(result$date),]

# Export the data to a csv file
write.csv(result, "./processed_data/model_data.csv", row.names = FALSE)

