import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Import CSV data
data = pd.read_csv('processed_data/uea_analysed.csv')

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Separate features and target variable
X = df.drop(columns=['date', 'wheat_ton_per_hectare'])
y = df['wheat_ton_per_hectare']

# Apply more weight to recent years by replicating them in the dataset
recent_years_count = 5
weight_factor = 5

# Identify the indices of recent years
recent_years_indices = df.tail(recent_years_count).index

# Use numpy repeat to replicate the indices of recent years
replicated_indices = np.repeat(recent_years_indices, weight_factor)

# Create new DataFrames by selecting the replicated indices
X_recent = X.loc[replicated_indices]
y_recent = y.loc[replicated_indices]

# Concatenate the original data with the replicated recent years
X_weighted = pd.concat([X, X_recent])
y_weighted = pd.concat([y, y_recent])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_weighted, y_weighted, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Make a prediction for the 2023 year (which is not in the dataset)
# Read the max and min values of each feature from the dataset
norm_dataset = pd.read_csv('processed_data/uea_converted.csv')
norm_gdd = pd.read_csv('processed_data/growing_season.csv')

# Get the max and min values of each feature
max_values = norm_dataset.max()
min_values = norm_dataset.min()

gdd_max = norm_gdd['gdd'].max()
gdd_min = norm_gdd['gdd'].min()

# Sample data for 2023
#potential_evapotranspiration,cloud_cover,precipitation,maximum_temperature,rain_days,minimum_temperature,vapour_pressure,ground_frost_frequency,diurnal_temperature_range,mean_temperature
# Take the average of the last 5 years for each feature
data_2023 = {
    'potential_evapotranspiration': (norm_dataset['potential_evapotranspiration'].tail(5*12).mean() - min_values['potential_evapotranspiration']) / (max_values['potential_evapotranspiration'] - min_values['potential_evapotranspiration']),
    'cloud_cover': (norm_dataset['cloud_cover'].tail(5*12).mean() - min_values['cloud_cover']) / (max_values['cloud_cover'] - min_values['cloud_cover']),
    'precipitation': (norm_dataset['precipitation'].tail(5*12).mean() - min_values['precipitation']) / (max_values['precipitation'] - min_values['precipitation']),
    'maximum_temperature': (norm_dataset['maximum_temperature'].tail(5*12).mean() - min_values['maximum_temperature']) / (max_values['maximum_temperature'] - min_values['maximum_temperature']),
    'rain_days': (norm_dataset['rain_days'].tail(5*12).mean() - min_values['rain_days']) / (max_values['rain_days'] - min_values['rain_days']),
    'minimum_temperature': (norm_dataset['minimum_temperature'].tail(5*12).mean() - min_values['minimum_temperature']) / (max_values['minimum_temperature'] - min_values['minimum_temperature']),
    'vapour_pressure': (norm_dataset['vapour_pressure'].tail(5*12).mean() - min_values['vapour_pressure']) / (max_values['vapour_pressure'] - min_values['vapour_pressure']),
    'ground_frost_frequency': (norm_dataset['ground_frost_frequency'].tail(5*12).mean() - min_values['ground_frost_frequency']) / (max_values['ground_frost_frequency'] - min_values['ground_frost_frequency']),
    'diurnal_temperature_range': (norm_dataset['diurnal_temperature_range'].tail(5*12).mean() - min_values['diurnal_temperature_range']) / (max_values['diurnal_temperature_range'] - min_values['diurnal_temperature_range']),
    'mean_temperature': (norm_dataset['mean_temperature'].tail(5*12).mean() - min_values['mean_temperature']) / (max_values['mean_temperature'] - min_values['mean_temperature']),
    'gdd': (norm_gdd['gdd'].tail(5).mean() - gdd_min) / (gdd_max - gdd_min)
}

# Get original wheat yield values
yield_data = pd.read_csv('processed_data/yield.csv')

yd = pd.DataFrame(yield_data)

yd = yd['wheat_ton_per_hectare']

# Get the average wheat yield
average_yield = yd.mean()

# Get the standard deviation of wheat yield
std_yield = yd.std()

print(f"Average wheat yield: {average_yield}")
print(f"Standard deviation of wheat yield: {std_yield}")

# Convert the input data for 2023 to a DataFrame
X_2023 = pd.DataFrame([data_2023])

# Predict the wheat yield for 2023
wheat_yield_2023 = model.predict(X_2023)

# Convert the predicted value to the original scale
wheat_yield_2023 = wheat_yield_2023 * std_yield + average_yield

print(f"Predicted wheat yield for 2023: {wheat_yield_2023[0]}")

# Enter your hectare value to get ton value
# hectare = float(input("Enter the hectare value: "))
hectare = 1

# calculate the wheat yield in tons
wheat_yield = hectare * wheat_yield_2023[0]

print(f"Wheat yield in tons: {wheat_yield}")

# Plot feature importance
importance = model.feature_importances_
feature_names = X.columns

plt.figure()
plt.barh(feature_names, importance)
plt.xlabel('Feature Importance')
plt.ylabel('Features')
plt.title('Feature Importance for Wheat Yield Prediction')
plt.show()

# Plot historical yields and predicted yield for 2023
historical_yields = yd.values
# Replace na values with 0
historical_yields = np.nan_to_num(historical_yields)
years = pd.to_datetime(df['date'], format='%Y').dt.year

# Reverse trim the historical yields to match the years
historical_yields = historical_yields[-len(years):]

plt.figure()
plt.plot(years, historical_yields, label='Historical Yields')
plt.scatter(2023, wheat_yield_2023, color='red', label='Predicted Yield for 2023')
plt.xlabel('Year')
plt.ylabel('Wheat Yield (ton/hectare)')
plt.title('Historical and Predicted Wheat Yields')
plt.legend()
plt.show()
