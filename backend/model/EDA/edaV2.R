library(ggplot2)
library(zoo)
library(corrplot)
library(reshape2)

# Load all the datasets
monthly <- read.csv("source/monthly.csv")
pentadal <- read.csv("source/pentadal.csv")
quarterly <- read.csv("source/quarterly.csv")
yearly <- read.csv("source/yearly.csv")

target <- read.csv("source/target.csv")

target$date <- as.Date(target$date)

# Plot target
ggplot(target, aes(x=date, y=wheat_ton_per_hectare)) +
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
ggplot(target, aes(x=date, y=wheat_ton_per_hectare)) +
  geom_line(aes(group=1), color="gray") +
  geom_line(aes(x=date, y=rolling_mean, group=1), color="red") +
  geom_ribbon(aes(x=date, ymin=ci_lower, ymax=ci_upper), fill="blue", alpha=0.2) +
  ggtitle("Target with Rolling Mean") +
  labs(
    x="Date",
    y="Wheat ton/ha",
    title="Target with Rolling Mean"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))


# Plot all variables in monthly on the same graph
monthly$date <- as.Date(monthly$date)

# normalize each variable
norm_monthly <- monthly

# Calculate rolling mean and standard deviation for each variable
for (i in 2:ncol(norm_monthly)) {
  norm_monthly[[i]] <- rollmean(norm_monthly[[i]], k = 5, fill = NA)
  norm_monthly[[i]] <- zoo::na.locf(norm_monthly[[i]], na.rm = FALSE)  # Forward fill
  norm_monthly[[i]] <- zoo::na.locf(norm_monthly[[i]], fromLast = TRUE)  # Backward fill
}


norm_monthly[, -1] <- scale(monthly[, -1])

monthly_melted <- melt(norm_monthly, id.vars = "date")

# For this scenario, only use last 5 years of data
monthly_melted <- monthly_melted[monthly_melted$date >= "2020-01-01", ]

ggplot(monthly_melted, aes(x=date, y=value, color=variable)) +
  geom_line() +
  ggtitle("Monthly Variables") +
  labs(
    x="Date",
    y="Value",
    title="Monthly Variables"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

# Plot a correlation matrix using corrplot
correlation_matrix <- cor(norm_monthly[, -1])
corrplot(correlation_matrix)


