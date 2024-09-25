library(ggplot2)
library(zoo)
library(corrplot)
library(reshape2)
library(dplyr)
library(tensorflow)
library(keras)

# Load all the datasets
monthly <- read.csv("source/monthly.csv")
pentadal <- read.csv("source/pentadal.csv")
quarterly <- read.csv("source/quarterly.csv")
yearly <- read.csv("source/yearly.csv")

target <- read.csv("source/target.csv")

target$date <- as.Date(target$date)

# Convert date to year
target$year <- as.numeric(format(target$date, "%Y"))

# Drop date column
target <- target %>%
  select(-date)

# Plot target
ggplot(target, aes(x=year, y=wheat_ton_per_hectare)) +
  geom_line(aes(group=1)) +
  ggtitle("Target") +
  labs(
    x="Date",
    y="Wheat ton per hectare",
    title="Target"
  ) +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme_minimal()

# Create rolling means for target
target$rolling_mean <- rollmean(target$wheat_ton_per_hectare, k = 5, fill = NA)
target$rolling_mean <- zoo::na.locf(target$rolling_mean, na.rm = FALSE)  # Forward fill
target$rolling_mean <- zoo::na.locf(target$rolling_mean, fromLast = TRUE)  # Backward fill

target$rolling_sd <- rollapply(target$wheat_ton_per_hectare, width = 5, FUN = sd, fill = NA)

n <- 5
# 95% confidence interval
critical_value <- qnorm(0.975)
target$margin_of_error <- critical_value * (target$rolling_sd / sqrt(n))

# Calculate confidence intervals
target$ci_lower <- target$rolling_mean - target$margin_of_error
target$ci_upper <- target$rolling_mean + target$margin_of_error

# View result
head(target)

target <- target[!is.na(target$rolling_mean), ]
target <- target[!is.na(target$ci_lower), ]
target <- target[!is.na(target$ci_upper), ]

# Plot target with rolling mean
ggplot(target, aes(x=year, y=wheat_ton_per_hectare)) +
  geom_line(aes(group=1), color="gray") +
  geom_line(aes(x=year, y=rolling_mean, group=1), color="red") +
  geom_ribbon(aes(x=year, ymin=ci_lower, ymax=ci_upper), fill="blue", alpha=0.2) +
  ggtitle("Target with Rolling Mean") +
  labs(
    x="Date",
    y="Wheat ton/ha",
    title="Target with Rolling Mean"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

train <- target[target$year < 2015, ]
test <- target[target$year >= 2015, ]

# Extract features and targets
train_features <- as.matrix(train[, !names(train) %in% c('year', 'wheat_ton_per_hectare')])
train_target <- train$wheat_ton_per_hectare
test_features <- as.matrix(test[, !names(test) %in% c('year', 'wheat_ton_per_hectare')])
test_target <- test$wheat_ton_per_hectare

# Define the model
model <- keras_model_sequential() %>%
  layer_dense(units=64, activation='relu', input_shape=ncol(train_features)) %>%
  layer_dense(units=1)

# Compile the model
model %>% compile(
  optimizer='adam',
  loss='mean_squared_error'
)

# Fit the model
model %>% fit(
  x = train_features,
  y = train_target,
  epochs = 100,  # Adjust epochs as needed
  batch_size = 32,
  validation_split = 0.2  # Use a validation split if desired
)

# Make predictions
predictions <- model %>% predict(test_features)

# Calculate RMSE
rmse <- sqrt(mean((test_target - predictions)^2))

# Combine actual values and predictions for plotting
results <- data.frame(
  year = test$year,
  actual = test_target,
  predicted = as.vector(predictions)  # Ensure predictions are in the right format
)

# Print RMSE
print(paste("RMSE:", rmse))


# Plot actual vs predicted
ggplot(results, aes(x=year)) +
  geom_line(aes(y=actual, color="Actual")) +
  geom_line(aes(y=predicted, color="Predicted"), linetype="dashed") +
  ggtitle(paste("RMSE:", round(rmse, 2))) +
  labs(
    x="Year",
    y="Wheat ton per hectare",
    title="Actual vs Predicted"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))


# Plot all variables in monthly on the same graph
monthly$date <- as.Date(monthly$date)

# normalize each variable
year_monthly <- monthly

# group by year
year_monthly$year <- as.numeric(format(year_monthly$date, "%Y"))

# year_monthly <- year_monthly %>%
#   group_by(year) %>%
#   summarize(across(-date, \(x) sum(x, na.rm = TRUE)))


# Colnames
# [1] "date"                         "potential_evapotranspiration" "cloud_cover"                  "precipitation"               
# [5] "maximum_temperature"          "rain_days"                    "minimum_temperature"          "vapour_pressure"             
# [9] "ground_frost_frequency"       "diurnal_temperature_range"    "mean_temperature" 

# Sum potential evapotranspiration
# Average cloud cover
# Sum precipitation
# Average max temperature
# Sum rain days
# Average min temperature
# Average vapour pressure
# Sum ground frost frequency
# Average diurnal temperature range
# Average mean temperature

year_monthly <- year_monthly %>%
  group_by(year) %>%
  summarize(
    potential_evapotranspiration = sum(potential_evapotranspiration, na.rm = TRUE),
    cloud_cover = mean(cloud_cover, na.rm = TRUE),
    precipitation = sum(precipitation, na.rm = TRUE),
    maximum_temperature = mean(maximum_temperature, na.rm = TRUE),
    rain_days = sum(rain_days, na.rm = TRUE),
    minimum_temperature = mean(minimum_temperature, na.rm = TRUE),
    vapour_pressure = mean(vapour_pressure, na.rm = TRUE),
    ground_frost_frequency = sum(ground_frost_frequency, na.rm = TRUE),
    diurnal_temperature_range = mean(diurnal_temperature_range, na.rm = TRUE),
    mean_temperature = mean(mean_temperature, na.rm = TRUE)
  )

# Merge yearly with target variable rolling_mean only
year_monthly <- merge(year_monthly, target, by="year")

# Drop rolling_sd, margin_of_error, ci_lower, ci_upper
year_monthly <- year_monthly %>%
  select(-c(rolling_mean, rolling_sd, margin_of_error, ci_lower, ci_upper))

# Predict target variable using all variables in monthly
# Split data into training and testing
train <- year_monthly[year_monthly$year < 2019, ]
test <- year_monthly[year_monthly$year >= 2019, ]

# Fit a SARIMA model
model <- arima(train$wheat_ton_per_hectare, order=c(1, 1, 1), seasonal=list(order=c(1, 1, 1), period=12))

# Make predictions on test data
n_test <- nrow(test)
predictions <- predict(model, n.ahead=n_test)$pred

# Calculate RMSE
rmse <- sqrt(mean((test$wheat_ton_per_hectare - predictions)^2))

# Combine actual values and predictions for plotting
results <- data.frame(
  year = test$year,
  actual = test$wheat_ton_per_hectare,
  predicted = predictions
)

# Plot actual vs predicted
ggplot(results, aes(x=year)) +
  geom_line(aes(y=actual, color="Actual")) +
  geom_line(aes(y=predicted, color="Predicted"), linetype="dashed") +
  ggtitle(paste("RMSE:", round(rmse, 2))) +
  labs(
    x="Year",
    y="Wheat ton per hectare",
    title="Actual vs Predicted"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

