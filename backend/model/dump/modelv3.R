library(tidyverse)
library(ggplot2)
library(gbm)

# Import processed_data/model_data_soil_moisture.csv
model_data_imputed <- read.csv("processed_data/model_data_soil_moisture.csv")

# Remove all columns that contain the word "soil" except for "soil_moisture"
model_data_imputed <- model_data_imputed %>%
  select(-contains("soil") | contains("soil_moisture"))

# Remove all ton_per_hectare columns except for "wheat_ton_per_hectare"
model_data_imputed <- model_data_imputed %>%
  select(-contains("ton_per_hectare") | contains("wheat_ton_per_hectare"))

# Convert date to date format
model_data_imputed$date <- as.Date(model_data_imputed$date)

# Add year column
model_data_imputed$year <- as.numeric(format(model_data_imputed$date, "%Y"))

# PLot wheat_ton_per_hectare vs year
model_data_imputed %>%
  ggplot(aes(x = year, y = wheat_ton_per_hectare)) +
  geom_line() +
  geom_smooth() +
  theme_minimal() +
  ggtitle("Wheat ton per hectare vs Year") +
  theme(legend.position = "bottom")

# Select last 10 years
model_data_imputed <- model_data_imputed %>%
filter(year >= 2010)

# Group data by year
model_data_imputed <- model_data_imputed %>%
  group_by(year) %>%
  summarise(across(everything(), mean, na.rm = TRUE))

model_data_imputed %>%
  ggplot(aes(x = year, y = wheat_ton_per_hectare)) +
  geom_line() +
  geom_smooth() +
  theme_minimal() +
  ggtitle("Wheat ton per hectare vs Year") +
  theme(legend.position = "bottom")


# 
# # Remove missing values
# model_data_imputed <- model_data_imputed %>%
#   drop_na()
# 
# # Drop satellite columns
# model_data_imputed <- model_data_imputed %>%
#   select(-contains("satellite"))
# 
# # Calculate GDD
# model_data_imputed$gdd <- (model_data_imputed$maximum_temperature + model_data_imputed$minimum_temperature) / 2 - 4
# 
# start_day <- 100  # April 21 (approx. day 111 of the year)
# end_day <- start_day + 100
# 
# # Add day_of_year column
# model_data_imputed$day_of_year <- as.numeric(format(model_data_imputed$date, "%j"))
# 
# # Filter rows based on the day_of_year
# model_data_imputed <- model_data_imputed %>%
#   filter(day_of_year >= start_day & day_of_year <= end_day)
# 
# # Remove day_of_year column
# model_data_imputed <- model_data_imputed %>%
#   select(-day_of_year)
# 
# # wheat_ton_per_hectare statistics
# summary(model_data_imputed$wheat_ton_per_hectare)
# 
# # Line graph of all columns
# model_data_imputed %>%
#   gather(key = "variable", value = "value", -c(date, year)) %>%
#   ggplot(aes(x = date, y = value, color = variable)) +
#   geom_line() +
#   facet_wrap(~variable, scales = "free") +
#   theme_minimal() +
#   labs(color = "Variable") +
#   ggtitle("Line graph of all variables") +
#   theme(legend.position = "bottom")
# 
# # Plot each year's graph on top of each other
# model_data_imputed %>%
#   gather(key = "variable", value = "value", -c(date, year)) %>%
#   ggplot(aes(x = value, color = as.factor(year))) +
#   geom_density() +
#   facet_wrap(~variable, scales = "free") +
#   theme_minimal() +
#   labs(color = "Year") +
#   ggtitle("Density plots of each variable across years") +
#   theme(legend.position = "bottom")
# 
# # Convert date to factor
# model_data_imputed$date <- as.factor(model_data_imputed$date)
# 
# # model
# set.seed(123)
# gbm_model <- gbm(wheat_ton_per_hectare ~ ., data = model_data_imputed, distribution = "gaussian", n.trees = 1000, interaction.depth = 10, shrinkage = 0.01)
# 
# # Predict for the same data
# model_data_imputed$gbm_fitted_values <- predict(gbm_model, model_data_imputed, n.trees = 1000)
# 
# future_years <- data.frame(year = max(model_data_imputed$year) + 1)
# 
# future_data <- model_data_imputed %>%
#   summarise(across(everything(), mean, na.rm = TRUE)) %>%
#   slice(rep(1, 5)) %>%
#   mutate(year = future_years$year)

# Predict for the next 5 years
# future_data$gbm_predicted_wheat_ton_per_hectare <- predict(gbm_model, future_data, n.trees = 1000)

# Plot actual, fitted, and predicted values
# ggplot() +
#   geom_line(data = model_data_imputed, aes(x = year, y = wheat_ton_per_hectare), color = "blue", size = 1, linetype = "dashed") + # Actual values
#   geom_line(data = model_data_imputed, aes(x = year, y = gbm_fitted_values), color = "red", size = 1) + # Fitted values
#   geom_line(data = future_data, aes(x = year, y = gbm_predicted_wheat_ton_per_hectare), color = "green", size = 1) + # Future predictions
#   theme_minimal() +
#   ggtitle("Wheat ton per hectare: Actual, Fitted, and Predicted with GBM") +
#   labs(x = "Year", y = "Wheat ton per hectare") +
#   theme(legend.position = "bottom")

# Plot a correlation matrix of all variables
# model_data_imputed %>%
#   select(-date, -year) %>%
#   cor() %>%
#   corrplot::corrplot(method = "color", type = "upper", order = "hclust", tl.col = "black")
# 
# # Compare all variables against model_data_imputed$wheat_ton_per_hectare
# model_data_imputed %>%
#   gather(key = "variable", value = "value", -c(date, year, wheat_ton_per_hectare)) %>%
#   ggplot(aes(x = value, y = wheat_ton_per_hectare)) +
#   geom_point() +
#   facet_wrap(~variable, scales = "free") +
#   theme_minimal() +
#   ggtitle("Scatter plots of each variable against wheat_ton_per_hectare") +
#   theme(legend.position = "bottom")
# 
# # Correlation summary with wheat_ton_per_hectare
# model_data_imputed %>%
#   select(-date, -year) %>%
#   cor() %>%
#   as.data.frame() %>%
#   filter(rownames(.) == "wheat_ton_per_hectare") %>%
#   gather(key = "variable", value = "correlation") %>%
#   arrange(desc(correlation))
# 
# # Save to CSV
# write.csv(model_data_imputed, "processed_data/model_data_imputed_v4.csv", row.names = FALSE)
