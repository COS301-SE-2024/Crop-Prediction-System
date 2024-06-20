# library(tidyverse)
# 
# # Import the data
# soil <- read.csv("./datasets/FAOSTAT_soildata.csv")
# 
# # Sort by year
# # soil <- soil[order(soil$Year),]
# 
# # Create a new dataframe
# df <- data.frame(Year = unique(soil$Year))
# 
# # Get distinct soil$Element
# elements <- unique(soil$Element)
# original_elements <- elements
# 
# # Remove "Cropland " from each element where an element is "Cropland ..."
# elements <- gsub("Cropland ", "", elements)
# 
# # Replace " " with "_"
# elements <- gsub(" ", "_", elements)
# 
# # Unique Item
# items <- unique(soil$Item)
# original_items <- items
# 
# # Convert the items to lowercase
# items <- tolower(items)
# 
# # Replace " " with "_"
# items <- gsub(" ", "_", items)
# 
# # Merge every element with every item (Meaning size of m*n)
# # Create a new column for each element and item
# # For each year, get the value of the element and item
# for (element in elements) {
#   for (item in items) {
#     df[[paste0(item, "_", element)]] <- NA
#   }
# }
# 
# # Add the elements as columns to the dataframe
# for (element in elements) {
#   df[[element]] <- NA
# }
# 
# # For each year, get the value of the element and item
# for (year in unique(soil$Year)) {
#   for (element in original_elements) {
#     for (item in original_items) {
#       value <- soil[soil$Element == element & soil$Item == item, "Value"]
#       value <- value[1]
#       item <- tolower(item)
#       item <- gsub(" ", "_", item)
#       element <- gsub("Cropland ", "", element)
#       element <- gsub(" ", "_", element)
#       col <- paste0(item, "_", element)
#       
#       # Insert the value into the correct row in the dataframe
#       df[df$Year == year, col] <- value
#     }
#   }
# }

library(tidyverse)

# Import the data
soil <- read.csv("./datasets/FAOSTAT_soildata.csv")

# Function to clean element names
clean_element <- function(element) {
  element <- gsub("Cropland ", "", element)
  element <- gsub(" ", "_", element)
  return(element)
}

# Function to clean item names
clean_item <- function(item) {
  item <- tolower(item)
  item <- gsub(" ", "_", item)
  return(item)
}

# Clean the elements and items
soil <- soil %>%
  mutate(Element = clean_element(Element),
         Item = clean_item(Item))

# Create a column for the combination of item and element
soil <- soil %>%
  mutate(Element_Item = paste0(Item, "_", Element))

# Pivot the data frame to wide format, ensuring missing values are filled with NA
df <- soil %>%
  select(Year, Element_Item, Value) %>%
  pivot_wider(names_from = Element_Item, values_from = Value, values_fill = NA) %>%
  arrange(Year)

# Remove columns with all NA values
df <- df %>%
  select(-where(~all(is.na(.))))

# Export the data frame to a csv file
write.csv(df, file = "./processed_data/soil.csv", row.names = FALSE)