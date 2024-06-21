import pandas as pd
import numpy as np

# Import the dataset
data = pd.read_csv('processed_data/model_data_imputed.csv')

# Convert the data to a DataFrame (this step is not necessary if 'data' is already a DataFrame)
dfResult = pd.DataFrame(data)

print(dfResult.columns)

# Now calculate the soil moisture %
# First calculate combined effect of precipitation and evapotranspiration for the next 16 days
dfResult['z_k'] = dfResult['precipitation'] / dfResult['potential_evapotranspiration']

# Normalize the dfResult['z_k'] column
dfResult['z_k'] = dfResult['z_k'] / dfResult['z_k'].max()

print(dfResult['z_k'])

# # Calculate the soil moisture by taking the average of the combined effect of precipitation and evapotranspiration for the next 1 entry
dfResult['soil_moisture'] = dfResult['z_k'].rolling(window=2).mean()

print(dfResult['soil_moisture'])

# Statistics
print(dfResult['soil_moisture'].describe())

# Drop the z_k column
dfResult.drop(columns=['z_k'], inplace=True)

# Save the data
dfResult.to_csv('processed_data/model_data_soil_moisture.csv', index=False)