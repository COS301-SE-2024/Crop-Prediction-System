library(ggplot2)
library(zoo)
library(corrplot)
library(reshape2)
library(dplyr)
library(tensorflow)
library(keras)
library(GGally)

# Load all the datasets
VC <- read.csv("visualcrossing.csv")
SB <- read.csv("field_data_rows.csv")

# rename VC's datetime column to date
names(VC)[names(VC) == "datetime"] <- "date"
names(VC)[names(VC) == "sealevelpressure"] <- "pressure"

# Rename columns
names(SB)[names(SB) == "dew_point"] <- "dew"
names(SB)[names(SB) == "uvi"] <- "uvindex"
names(SB)[names(SB) == "pop"] <- "precipprob"
names(SB)[names(SB) == "rain"] <- "precip"
names(SB)[names(SB) == "clouds"] <- "cloudcover"

# Merge the datasets on date
merged <- merge(VC, SB, by="date")

# colnames(merged)
# [1] "date"         "tempmax.x"    "tempmin.x"    "dew.x"        "humidity.x"   "precip.x"     "precipprob.x" "pressure.x"  
# [9] "cloudcover.x" "uvindex.x"    "tempmax.y"    "tempmin.y"    "pressure.y"   "humidity.y"   "dew.y"        "cloudcover.y"
# [17] "precipprob.y" "precip.y"     "uvindex.y"  


# Plot all variables with date as x-axis
ggplot(merged, aes(x=date)) +
  # error line of tempmax.x against tempmax.y
  geom_bar(aes(y=tempmax.x), stat="identity", fill="blue", alpha=0.5) +
  geom_bar(aes(y=tempmax.y), stat="identity", fill="red", alpha=0.5) +
  geom_errorbar(aes(ymin=tempmax.x, ymax=tempmax.y), width=0.2) +
  ggtitle("All variables") +
  labs(
    x="Date",
    y="Value",
    title="All variables"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(angle = 45, hjust = 1)
  ) +
  theme_minimal()

# Scatter plot of tempmin.x and tempmin.y
ggplot(merged, aes(x=tempmin.x, y=tempmin.y)) +
  geom_point() +
  ggtitle("Scatter plot of tempmin.x and tempmin.y") +
  labs(
    x="tempmin.x",
    y="tempmin.y",
    title="Scatter plot of tempmin.x and tempmin.y"
  ) +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme_minimal()

# Linear model predicting tempmax based on tempmin.x and tempmin.y
model <- lm(tempmin.x ~ tempmin.y, data = merged)

# Summary of the model
summary(model)

# Plot the model
ggplot(merged, aes(x=tempmin.y, y=tempmin.x)) +
  geom_point() +
  geom_smooth(method="lm", se=FALSE) +
  ggtitle("Linear model predicting tempmin.x based on tempmin.y") +
  labs(
    x="tempmin.y",
    y="tempmin.x",
    title="Linear model predicting tempmin.x based on tempmin.y"
  ) +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme_minimal()

merged <- merged %>%
  select(-c("gff","gdd","hdd","soil_moisture","soil_temperature","pet","health","sprayability","yield","solarradiation","wind_gust","wind_speed","wind_deg","visibility", "field_id", "summary", "tempdiurnal", "tempmean", "temp"))

colnames(merged)

# colnames(merged)
# [1] "date"         "tempmax.x"    "tempmin.x"    "dew.x"        "humidity.x"   "precip.x"     "precipprob.x" "pressure.x"  
# [9] "cloudcover.x" "uvindex.x"    "tempmax.y"    "tempmin.y"    "pressure.y"   "humidity.y"   "dew.y"        "cloudcover.y"
# [17] "precipprob.y" "precip.y"     "uvindex.y"  

# corrplot but only keep values that are greater than 0.5
correlation_matrix <- cor(merged[,2:18])
correlation_matrix[correlation_matrix < 0.5] <- 0

# corrplot(correlation_matrix, method="number", type="lower", tl.col="black")
# corrplot(correlation_matrix, method="number", , tl.col="black", tl.srt=45)


