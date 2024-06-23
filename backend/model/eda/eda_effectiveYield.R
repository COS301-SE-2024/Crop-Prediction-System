library(ggplot2)

# Read effective_yield.csv
effective_yield <- read.csv("effective_yield.csv")

# Print the first few rows of the data
head(effective_yield)

# Print the structure of the data
str(effective_yield)

# Print the summary of the data
summary(effective_yield)

# Convert the date column to a date object
effective_yield$date <- as.Date(effective_yield$date)

# Plot the effective yield against the date
ggplot(effective_yield, aes(x=date, y=effective_yield)) +
  geom_line() +
  ggtitle("Effective Yield over Time") +
  xlab("Time") + ylab("Effective Yield") +
  scale_x_date(date_breaks = "1 year", date_labels = "%b %Y") +
  theme_minimal()

# Select data from 2012 onwards
effective_yield <- effective_yield[effective_yield$date > "2012-01-01", ]

# Plot the effective yield from 2012 onwards
ggplot(effective_yield, aes(x=date, y=effective_yield)) +
  geom_line() +
  ggtitle("Effective Yield from 2012 onwards") +
  xlab("Time") + ylab("Effective Yield") +
  scale_x_date(date_breaks = "1 year", date_labels = "%b %Y") +
  theme_minimal()