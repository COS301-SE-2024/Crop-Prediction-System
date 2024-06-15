# Plot all the columns
library(ggplot2)
library(corrplot)
library(dplyr)
library(reshape2)

data <- read.csv("uea_converted.csv")
yield <- read.csv("yield.csv")
growing_season <- read.csv("growing_season.csv")

# Convert growing season date from 1950-07 to 1950
growing_season$year <- as.numeric(substr(growing_season$year, 1, 4))

# First column is in the format 1911/12, meaning 1911-1912. Take the first year
yield$production_year <- as.Date(paste0("01-01-", substr(yield$production_year, 1, 4)), format = "%d-%m-%Y")

# Convert production year to match the year in data_melted
yield$production_year <- as.numeric(format(yield$production_year, "%Y"))

# Make a new dataframe only containing the wheat yield and production year
wheat_yield <- yield[, c("production_year", "wheat_ton_per_hectare")]

# First column is the date in the format FEB-2020 which is month and year
# Convert it to a date object
data$date <- as.Date(paste0("01-", data$date), format = "%d-%b-%Y")

# Convert the date to year
data$date <- as.numeric(format(data$date, "%Y"))

# Group by year and take the mean of all the columns
data <- data %>%
  group_by(date) %>%
  summarise_all(mean)

# Add the wheat yield to the data
data <- merge(data, wheat_yield, by.x = "date", by.y = "production_year")

# Add the growing season to the data
data <- merge(data, growing_season, by.x = "date", by.y = "year")

# Normalize the data
data <- data %>%
  mutate_at(vars(-date), scale)

# # Remove rows with NA values
data_analyse <- data[complete.cases(data), ]

# Save data_analyse as csv
write.csv(data_analyse, "datasets/uea_analysed.csv", row.names = FALSE)

# Correlation between wheat yield and other columns
correlation <- cor(data_analyse)

# Plot the correlation map between wheat yield and other columns
corrplot(correlation, type = "upper", order = "hclust", 
         tl.col = "black", tl.srt = 45)

# Melt the data
data_melted <- melt(data, id.vars = "date")

# Select the last 15 years
data_melted <- data_melted[data_melted$date > 2012, ]

# Plot the data and make wheat yield stand out
ggplot(data_melted, aes(x = date, y = value, color = variable)) +
  geom_line() +
  geom_line(data = data_melted[data_melted$variable == "wheat_ton_per_hectare", ], aes(x = date, y = value, color = variable), size = 1.5) +
  geom_point(data = data_melted[data_melted$variable == "gdd", ], aes(x = date, y = value, color = variable), size = 2) +
  labs(title = "Wheat yield and other data over time",
       x = "Year",
       y = "Value",
       color = "Legend") +
  theme_minimal()

# Perform regression analysis
model <- lm(wheat_ton_per_hectare ~ ., data = data_analyse)

# Show the summary of the model
summary(model)

# Plot the residuals
plot(model$residuals)

# Plot the residuals against the fitted values
plot(model$fitted.values, model$residuals)

# Plot the residuals against the wheat yield
plot(data_analyse$wheat_ton_per_hectare, model$residuals)

# Predict the wheat yield
predicted_yield <- predict(model, data_analyse)

# Plot the predicted yield against the actual yield
ggplot(data_analyse, aes(x = wheat_ton_per_hectare, y = predicted_yield)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "red")
  labs(title = "Predicted yield vs actual yield",
       x = "Actual yield",
       y = "Predicted yield") +
  theme_minimal()

# Perform random forest analysis
library(randomForest)

# Remove the date column
data_analyse <- data_analyse[, -1]

# Split the data into training and testing
set.seed(123)
train_index <- sample(1:nrow(data_analyse), 0.8 * nrow(data_analyse))
train_data <- data_analyse[train_index, ]
test_data <- data_analyse[-train_index, ]

# Train the random forest model
model_rf <- randomForest(wheat_ton_per_hectare ~ ., data = train_data, ntree = 500)

# Predict the wheat yield
predicted_yield_rf <- predict(model_rf, test_data)

# Plot the predicted yield against the actual yield
ggplot(data = test_data, aes(x = wheat_ton_per_hectare, y = predicted_yield_rf)) +
  geom_point() +
  geom_abline(intercept = 0, slope = 1, color = "red") +
  labs(title = "Random forest predicted yield vs actual yield",
       x = "Actual yield",
       y = "Predicted yield") +
  theme_minimal()


