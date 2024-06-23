library(ggplot2)
library(lubridate)
library(zoo)
library(corrplot)
library(dplyr)
library(reshape2)

# Load data
data <- read.csv("ndvi_data.csv")

# Load PET and CHIRPS data
pet_data <- read.csv("datasets/pet_data.csv")
chirps_data <- read.csv("datasets/chirps_data_interpolated.csv")

# Load csi data
csi_data <- read.csv("effective_yield.csv")

# Select csi data from 2012 onwards
csi_data <- csi_data[csi_data$date > "2012-02-01", ]

# Manually align the PET and CHIRPS data with the NDVI data
PETrange <- nrow(data) + 7
CHIRPSrange <- nrow(data) + 6

percentageComplete <- (nrow(data) / nrow(chirps_data)) * 100

# Add PET and CHIRPS data to the NDVI data but only select as much as data allows
data$PETmean <- pet_data$mean[8:PETrange] 
data$PETstd <- pet_data$std[8:PETrange]
data$CHIRPSmean <- chirps_data$mean[7:CHIRPSrange]
data$CHIRPSstd <- chirps_data$std[7:CHIRPSrange]
data$CSI <- csi_data$effective_yield[1:nrow(data)]
data$date <- as.Date(data$date)

# Create a new dataframe to eventually save as csv
newData <- data.frame(date = data$date, NDVImean = data$mean, NDVIstd = data$std, PETmean = data$PETmean, PETstd = data$PETstd, CHIRPSmean = data$CHIRPSmean, CHIRPSstd = data$CHIRPSstd, CSI = data$CSI)

# Save the new data to a csv file
write.csv(newData, "datasets/combined_data.csv", row.names = FALSE)

# Normalise the means by using z-scores
data$mean <- scale(data$mean)
data$PETmean <- scale(data$PETmean)
data$CHIRPSmean <- scale(data$CHIRPSmean)
data$CSI <- scale(data$CSI)

# Plot the data with all 3 means and add csi to the background
ggplot(data, aes(x=date)) +
  geom_smooth(aes(y = PETmean, color = "Evapotranspiration (Water lost)", group = 1)) +
  geom_line(aes(y = CHIRPSmean, color = "Rainfall (Precipitation)", group = 1)) +
  geom_line(aes(y = mean, color = "Vegetation Index", group = 1)) +
  geom_line(aes(y=CSI, color="CSI"), alpha=0.2) +
  ggtitle("NDVI, PET, CHIRPS and CSI over Time") +
  xlab("Time") + ylab("Normalized Value") +
  scale_color_manual(values=c("Vegetation Index"="darkgreen", "Evapotranspiration (Water lost)"="red", "Rainfall (Precipitation)"="blue", "CSI"="black")) +
  scale_x_date(date_breaks = "1 year", date_labels = "%b %Y") +
  theme_minimal()

# Correlation between NDVI and PET
cor(data$mean, data$PETmean)

# Correlation between NDVI and CHIRPS
cor(data$mean, data$CHIRPSmean)

# Correlation between PET and CHIRPS
cor(data$PETmean, data$CHIRPSmean)

# Interpreting the correlation values
# Good NDVI follows a period after CHIRPS. The delay is due to the time it takes for vegetation to grow after rainfall.
# The correlation between NDVI and PET is positive, which is expected as vegetation growth requires water.
# Low correlation between PET and NDVI is expected as PET is a measure of water loss, not vegetation growth.

# Identify the outliers and show their date
(outliers <- data[which(data$mean > 2 | data$mean < -2), ])

# Plot the data with all 3 means and add csi to the background
ggplot(data, aes(x=date)) +
  geom_smooth(aes(y = PETmean, color = "Evapotranspiration (Water lost)", group = 1)) +
  geom_line(aes(y = CHIRPSmean, color = "Rainfall (Precipitation)", group = 1)) +
  geom_line(aes(y = mean, color = "Vegetation Index", group = 1)) +
  geom_line(aes(y=CSI, color="CSI"), alpha=0.2) +
  ggtitle("NDVI, PET, CHIRPS and CSI over Time") +
  xlab("Time") + ylab("Normalized Value") +
  scale_color_manual(values=c("Vegetation Index"="darkgreen", "Evapotranspiration (Water lost)"="red", "Rainfall (Precipitation)"="blue", "CSI"="black")) +
  scale_x_date(date_breaks = "1 year", date_labels = "%b %Y") +
  theme_minimal()

# Convert date to timestamp
newData$date <- as.numeric(as.POSIXct(newData$date))

# Fill in the missing values
newData <- na.locf(newData)

# Normalise the newData except the date
newData <- newData %>%
  mutate_at(vars(-date), scale)

# Select only the means, date and csv in a new dataframe
newDF <- newData[, c("date", "NDVImean", "PETmean", "CHIRPSmean", "CSI")]

# Make a correlation between the means and CSI
(correlation <- cor(newDF))

# corrplot
corrplot(correlation, type = "upper", order = "hclust", 
         tl.col = "black", tl.srt = 45)
