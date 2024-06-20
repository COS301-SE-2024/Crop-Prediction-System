import pandas as pd
from knn_function import knn_impute

# Import CSV data
data = pd.read_csv('processed_data/model_data_imputed.csv')

# Convert the data to a DataFrame
df = pd.DataFrame(data)

df = df.drop(columns=['maize_ton_per_hectare', 'maize_comm_ton_per_hectare', 'maize_non_comm_ton_per_hectare', 'wheat_ton_per_hectare', 'groundnuts_ton_per_hectare', 
'sunflowerseed_ton_per_hectare', 'sorghum_ton_per_hectare', 'soybeans_ton_per_hectare', 'barley_ton_per_hectare', 'canola_ton_per_hectare', 'oats_ton_per_hectare'])

# Import KNN model
norm_dataset = df

max_values = norm_dataset.max()
min_values = norm_dataset.min()

# Sample User input
data_2023 = {
    'date': '2023-01-01',
    'potential_evapotranspiration': norm_dataset['potential_evapotranspiration'].tail(5*12).mean(),
    'cloud_cover': norm_dataset['cloud_cover'].tail(5*12).mean(),
    'precipitation': norm_dataset['precipitation'].tail(5*12).mean(),
    'maximum_temperature': norm_dataset['maximum_temperature'].tail(5*12).mean(),
    'rain_days': norm_dataset['rain_days'].tail(5*12).mean(),
    'minimum_temperature': norm_dataset['minimum_temperature'].tail(5*12).mean(),
    'vapour_pressure': norm_dataset['vapour_pressure'].tail(5*12).mean(),
    'ground_frost_frequency': norm_dataset['ground_frost_frequency'].tail(5*12).mean(),
    'diurnal_temperature_range': norm_dataset['diurnal_temperature_range'].tail(5*12).mean(),
    'mean_temperature': norm_dataset['mean_temperature'].tail(5*12).mean(),
}

# Convert the input data for 2023 to a DataFrame
X_2023 = pd.DataFrame([data_2023])

# Create a combined DataFrame
combined_df = pd.concat([df, X_2023], ignore_index=True)

print("Combined DataFrame:")
print(combined_df.tail())

# Impute missing values using KNN
df_imputed = knn_impute(combined_df)