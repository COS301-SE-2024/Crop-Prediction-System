library(dplyr)
library(ggplot2)
library(tidyr)
library(corrplot)
library(randomForest)
library(zoo)

# Import uea_converted.csv
uea <- read.csv("uea_converted.csv")

# Convert date column to Date format
uea$date <- as.Date(uea$date, format = "%d-%b-%Y")

# Convert date to year
uea$year <- as.numeric(format(uea$date, "%Y"))

# Add day of the year
uea$day <- as.numeric(format(as.Date(uea$date), "%j"))

# Rename potential_evapotranspiration column to pet
uea <- rename(uea, pet = potential_evapotranspiration)

# tBase is the base temperature for wheat
tBase <- 5

# Group the data into 4 stages: early, mid, late, and post growing season
uea$stage <- cut(uea$day, breaks = c(111, 151, 182, 243, 304, 365), 
                 labels = c("sowing", "germination", "tillering", "heading", "maturity"))

# Add GDD
uea$gdd <- with(uea, pmax(0, (maximum_temperature + minimum_temperature) / 2 - tBase))

# Add HDD
uea$hdd <- with(uea, pmax(0, mean_temperature - tBase))

# Remove stages with missing values
uea <- na.omit(uea)

# Aggregate the data by stage but yearly
uea_avg <- aggregate(cbind(pet, cloud_cover, maximum_temperature, 
                           minimum_temperature, vapour_pressure, diurnal_temperature_range, 
                           mean_temperature) ~ stage + year, data = uea, FUN = mean, na.rm = TRUE)

# Aggregate sum for specific variables
uea_sum <- aggregate(cbind(precipitation, rain_days, ground_frost_frequency, gdd, hdd) ~ stage + year, 
                     data = uea, FUN = sum, na.rm = TRUE)

# Merge the averaged and summed data into a single data frame
uea_yearly <- merge(uea_avg, uea_sum, by = c("stage", "year"))

# Sort the data by year and stage
uea_yearly <- uea_yearly[order(uea_yearly$year, uea_yearly$stage),]

# Import combined_data
# combined_data <- read.csv("combined_data.csv")
# 
# # Use only NDVI_mean and PET_mean
# combined_data <- combined_data[, c("date", "NDVImean", "PETmean")]
# 
# # Add day of the year
# combined_data$day <- as.numeric(format(as.Date(combined_data$date), "%j"))
# 
# # Convert date to year
# combined_data$year <- as.numeric(format(as.Date(combined_data$date), "%Y"))
# 
# # Group the data into 4 stages: early, mid, late, and post growing season
# combined_data$stage <- cut(combined_data$day, breaks = c(111, 151, 182, 243, 304, 365), 
#                             labels = c("sowing", "germination", "tillering", "heading", "maturity"))
# 
# # Remove stages with missing values
# combined_data <- na.omit(combined_data)
# 
# # Aggregate the data by stage but yearly
# combined_avg <- aggregate(cbind(NDVImean, PETmean) ~ stage + year, data = combined_data, FUN = mean, na.rm = TRUE)
# 
# # Merge the averaged data with the aggregated weather data
# uea_combined <- merge(uea_yearly, combined_avg, by = c("stage", "year"))

# Import the crop yield data (yield.csv)
yield <- read.csv("yield.csv")

# Select wheat_ton_per_hectare column
yield_wheat <- yield[, c("production_year", "wheat_ton_per_hectare")]

# Convert year column to numeric (it is 2011/12, change to 2012)
yield_wheat$year <- as.numeric(substring(yield_wheat$production_year, 1, 4)) + 1

# Remove production_year column
yield_wheat <- yield_wheat[, c("year", "wheat_ton_per_hectare")]

# Calculate the lagged yield for prediction
# yield_wheat$wheat_ton_per_hectare_lag <- yield_wheat$wheat_ton_per_hectare - lag

# Remove rows with missing values
yield_wheat <- na.omit(yield_wheat)

# Merge the yield data with the aggregated weather data
uea_yield <- merge(uea_yearly, yield_wheat, by = "year")

# Feature Engineering
# Cumulative precipitation but reset at the beginning of each year
uea_yield$cumulative_precipitation <- ave(uea_yield$precipitation, uea_yield$year, FUN = cumsum)

# Soil moisture index
uea_yield$soil_moisture_index <- with(uea_yield, (pet - precipitation) / pet)
# negative values indicate that the soil is wetter than the potential evapotranspiration, while positive values indicate that the soil is drier.

# Soil temperature index
uea_yield$soil_temperature_index <- with(uea_yield, (maximum_temperature + minimum_temperature) / 2)

# UV index
# UV radiation generally increases with temperature and decreases with cloud cover.
uea_yield$uv_index <- with(uea_yield, (maximum_temperature - minimum_temperature) / cloud_cover)

# Remove rows with missing values
uea_yield <- na.omit(uea_yield)

# Change wheat_ton_per_hectare to ton_per_hectare
uea_yield <- rename(uea_yield, ton_per_hectare = wheat_ton_per_hectare)

# Convert wide data to long format
uea_yield_long <- uea_yield %>%
  pivot_longer(cols = -c(year, stage, ton_per_hectare), names_to = "variable", values_to = "value")

# Boxplot of weather variables by growing season stage
ggplot(uea_yield_long, aes(x = stage, y = value, color = variable)) +
  geom_boxplot() +
  facet_wrap(~variable, scales = "free_y") +
  labs(title = "Weather Variables by Growing Season Stage",
       x = "Stage",
       y = "Value") +
  theme_minimal()

# Split the data into 4 stages
uea_stage <- split(uea_yield, uea_yield$stage)

ggplot(uea_yield, aes(x = year, y = ton_per_hectare)) +
  geom_line(color = "blue") +
  geom_smooth(method = "lm", se = FALSE) +
  labs(title = "Trend of Wheat Yield Over the Years",
       x = "Year",
       y = "Wheat Ton per Hectare") +
  theme_minimal()

# Plot trends for individual weather variables
ggplot(uea_yield_long, aes(x = year, y = value, color = variable)) +
  geom_line() +
  facet_wrap(~variable, scales = "free_y") +
  labs(title = "Trends of Weather Variables Over Years",
       x = "Year",
       y = "Value") +
  theme_minimal()

library(corrplot)

library(randomForest)

# Exclude year and stage columns
uea_stage <- lapply(uea_stage, function(x) x[, -c(1, 2)])

# Set seed for reproducibility
set.seed(123)

# Sowing Stage
rf_sowing <- randomForest(ton_per_hectare ~ ., data = uea_stage$sowing, importance = TRUE)

# Germination Stage
rf_germination <- randomForest(ton_per_hectare ~ ., data = uea_stage$germination, importance = TRUE)

# Tillering Stage
rf_tillering <- randomForest(ton_per_hectare ~ ., data = uea_stage$tillering, importance = TRUE)

# Heading Stage
rf_heading <- randomForest(ton_per_hectare ~ ., data = uea_stage$heading, importance = TRUE)

# Maturity Stage
rf_maturity <- randomForest(ton_per_hectare ~ ., data = uea_stage$maturity, importance = TRUE)

# Extract importance for each stage
importance_sowing <- importance(rf_sowing)
importance_sowing_df <- data.frame(Variable = rownames(importance_sowing), Importance = importance_sowing)

importance_germination <- importance(rf_germination)
importance_germination_df <- data.frame(Variable = rownames(importance_germination), Importance = importance_germination)

importance_tillering <- importance(rf_tillering)
importance_tillering_df <- data.frame(Variable = rownames(importance_tillering), Importance = importance_tillering)

importance_heading <- importance(rf_heading)
importance_heading_df <- data.frame(Variable = rownames(importance_heading), Importance = importance_heading)

importance_maturity <- importance(rf_maturity)
importance_maturity_df <- data.frame(Variable = rownames(importance_maturity), Importance = importance_maturity)

## Combine importance data for all stages
importance_combined <- rbind(
  data.frame(Stage = "1: Sowing", importance_sowing_df),
  data.frame(Stage = "2: Germination", importance_germination_df),
  data.frame(Stage = "3: Tillering", importance_tillering_df),
  data.frame(Stage = "4: Heading", importance_heading_df),
  data.frame(Stage = "5: Maturity", importance_maturity_df)
)

# Rename columns for consistency
importance_combined <- importance_combined %>%
  rename(Importance = Importance.IncNodePurity) # Use whichever column is appropriate

# Remove # Remove Importance..IncMSE column
importance_combined <- importance_combined %>%
  select(-starts_with("Importance.."))


# Plot importance for all stages but keep stage order consistent
ggplot(importance_combined, aes(x = reorder(Variable, Importance), y = Importance, fill = Stage)) +
  geom_bar(stat = "identity", position = "dodge") +
  coord_flip() +
  labs(title = "Variable Importance for Each Stage",
       x = "Weather Variable",
       y = "Importance") +
  theme_minimal() +
  facet_wrap(~Stage, scales = "free_y")

# Write input data to CSV
# Drop ton_per_hectare column
uea_yield <- uea_yield[, -which(names(uea_yield) == "ton_per_hectare")]
write.csv(uea_yield, "uea_yield.csv", row.names = FALSE)

# Change format of importance_combined to wide format
importance_combined_wide <- importance_combined %>%
  pivot_wider(names_from = Stage, values_from = Importance)

# Save wide as CSV
write.csv(importance_combined_wide, "importance_combined.csv", row.names = FALSE)
