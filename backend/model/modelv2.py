import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_squared_log_error, median_absolute_error, explained_variance_score
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import inquirer

from backend.model.cropHealth import calculateHealth
optimums = pd.read_csv('misc/optimums.csv')
optimums = pd.DataFrame(optimums)

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Time Metrics
import time
times = []

data = pd.read_csv('processed_data/model_data_soil_moisture.csv')

crops = [
    'maize',
    'maize_comm',
    'maize_non_comm',
    'wheat',
    'groundnuts',
    'sunflowerseed',
    'sorghum',
    'soybeans',
    'barley',
    'canola',
    'oats'
]

# Create a question for multi-choice selection
questions = [
    inquirer.List(
        'selected_crops',
        message="Select the crops you are interested in",
        choices=crops,
    ),
]

# Prompt the user to select crops
answer = inquirer.prompt(questions)
crop = answer['selected_crops']
crop = crop + '_ton_per_hectare'
crops = [c + '_ton_per_hectare' for c in crops]

# Print the selected crops
print("\n\033[93m" + "Selected Crops" + "\033[0m")
print(crop)

start_time = time.time()
# Convert the data to a DataFrame
df = pd.DataFrame(data)

other_crops = [c for c in crops if c != crop]

# Ignore other crops but wheat
df = df.drop(columns=other_crops)

# Select all rows where wheat_ton_per_hectare is not null
df = df[df[crop].notnull()]

# Separate features and target variable
X = df.drop(columns=['date', crop])
y = df[crop]


# Normalize the data
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_weighted = scaler_X.fit_transform(X)
y_weighted = scaler_y.fit_transform(y.values.reshape(-1, 1))

# print(X_weighted)

# Create sequences for the LSTM model
def create_sequences(X, y, seq_length):
    Xs, ys = [], []
    for i in range(len(X) - seq_length):
        Xs.append(X[i:i+seq_length])
        ys.append(y[i+seq_length])
    return np.array(Xs), np.array(ys)

seq_length = 10
X_seq, y_seq = create_sequences(X_weighted, y_weighted, seq_length)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

# Define the LSTM model
model = Sequential()
model.add(Input(shape=(seq_length, X_train.shape[2])))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

end_time = time.time()
times.append(end_time - start_time)
start_time = time.time()

# Train the LSTM model
history = model.fit(X_train, y_train, epochs=250, validation_split=0.2, batch_size=24)

# Evaluate the model
y_pred = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred)
y_test = scaler_y.inverse_transform(y_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
msle = mean_squared_log_error(y_test, y_pred)
medae = median_absolute_error(y_test, y_pred)
evs = explained_variance_score(y_test, y_pred)

# Print in green statistics
print("\n\033[92m" + "Model evaluation" + "\033[0m")


print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Log Error: {msle}")
print(f"Median Absolute Error: {medae}")
print(f"Explained Variance Score: {evs}")

print("\n")


# Show feature importance
# importance = model.layers[0].get_weights()[0]
# feature_importance = np.mean(importance, axis=1)

# features = ['potential_evapotranspiration', 'cloud_cover', 'precipitation', 'maximum_temperature', 'rain_days', 'minimum_temperature', 'vapour_pressure', 'ground_frost_frequency', 'diurnal_temperature_range', 'mean_temperature', 'soil_moisture', 'soil_mineral_fertilizers_nitrogen', 'soil_mineral_fertilizers_nitrogen_per_unit_area', 'soil_mineral_fertilizers_phosphorus', 'soil_mineral_fertilizers_phosphorus_per_unit_area', 'soil_mineral_fertilizers_potassium', 'soil_mineral_fertilizers_potassium_per_unit_area', 'soil_manure_applied_to_soils_nitrogen', 'soil_manure_applied_to_soils_nitrogen_per_unit_area', 'soil_manure_applied_to_soils_phosphorus', 'soil_manure_applied_to_soils_phosphorus_per_unit_area', 'soil_manure_applied_to_soils_potassium', 'soil_manure_applied_to_soils_potassium_per_unit_area', 'soil_atmospheric_deposition_nitrogen', 'soil_atmospheric_deposition_nitrogen_per_unit_area', 'soil_crop_removal_nitrogen', 'soil_crop_removal_nitrogen_per_unit_area', 'soil_crop_removal_phosphorus', 'soil_crop_removal_phosphorus_per_unit_area', 'soil_crop_removal_potassium', 'soil_crop_removal_potassium_per_unit_area', 'soil_biological_fixation_nitrogen', 'soil_biological_fixation_nitrogen_per_unit_area', 'soil_seed_nitrogen', 'soil_seed_nitrogen_per_unit_area', 'soil_seed_phosphorus', 'soil_seed_phosphorus_per_unit_area', 'soil_leaching_nitrogen', 'soil_leaching_nitrogen_per_unit_area', 'soil_volatilisation_nitrogen', 'soil_volatilisation_nitrogen_per_unit_area', 'satellite_NDVImean', 'satellite_NDVIstd', 'satellite_PETmean', 'satellite_PETstd', 'satellite_CHIRPSmean', 'satellite_CHIRPSstd']

# plt.bar(features, feature_importance)
# plt.xticks(rotation=45)
# plt.ylabel('Feature Importance')
# plt.title('Feature Importance for Wheat Yield Prediction')
# plt.show()

# # Plot predicted vs actual wheat yield
# plt.plot(y_test, label='Actual')
# plt.plot(y_pred, label='Predicted')
# plt.legend()
# plt.title('Predicted vs Actual Wheat Yield')
# plt.show()

# Save the model
model.save('yield_prediction_model.keras')
# print("Model saved successfully")

end_time = time.time()
times.append(end_time - start_time)
start_time = time.time()

# Import KNN model
norm_dataset = df

max_values = norm_dataset.max()
min_values = norm_dataset.min()

# Sample User input
data_2023 = {
    'date': '2023-01-01',
    'potential_evapotranspiration': norm_dataset['potential_evapotranspiration'].tail(15*12).mean(),
    'cloud_cover': norm_dataset['cloud_cover'].tail(15*12).mean(),
    'precipitation': norm_dataset['precipitation'].tail(15*12).mean(),
    'maximum_temperature': norm_dataset['maximum_temperature'].tail(15*12).mean(),
    'rain_days': norm_dataset['rain_days'].tail(15*12).mean(),
    'minimum_temperature': norm_dataset['minimum_temperature'].tail(15*12).mean(),
    'vapour_pressure': norm_dataset['vapour_pressure'].tail(15*12).mean(),
    'ground_frost_frequency': norm_dataset['ground_frost_frequency'].tail(15*12).mean(),
    'diurnal_temperature_range': norm_dataset['diurnal_temperature_range'].tail(15*12).mean(),
    'mean_temperature': norm_dataset['mean_temperature'].tail(15*12).mean()
}

# Convert the input data for 2023 to a DataFrame
X_2023 = pd.DataFrame([data_2023])

from knn_function import knn_impute

# Create a combined DataFrame
combined_df = pd.concat([df, X_2023], ignore_index=True)

# print("Combined DataFrame:")
# print(combined_df.tail())

# Impute missing values using KNN
df_imputed = knn_impute(combined_df)

end_time = time.time()
times.append(end_time - start_time)
start_time = time.time()

# print("Imputed DataFrame:")
# print(df_imputed.tail())

# Replace X_2023 with the imputed values
X_2023 = df_imputed.tail(1)

# print("Imputed X_2023:")
# print(X_2023)

# Ensure the input data for 2023 is the same as the training data
X_2023 = X_2023.drop(columns=[crop])

# Add feature names to X_2023 to match the training data
X_2023 = X_2023[X.columns]

# Ensure the input data for 2023 has the correct sequence length
X_2023_seq = []
for i in range(seq_length):
    X_2023_seq.append(X_2023.values.flatten())
X_2023_seq = np.array(X_2023_seq).reshape((1, seq_length, X_2023.shape[1]))

# Reshape the data for the LSTM model
X_2023_seq = scaler_X.transform(X_2023_seq.reshape(-1, X_2023.shape[1]))
X_2023_seq = X_2023_seq.reshape((1, seq_length, X_2023.shape[1]))

# X doesn't have valid feature names
X_2023 = X_2023[X.columns]

# Predict the wheat yield for 2023
wheat_yield_2023 = model.predict(X_2023_seq)
wheat_yield_2023 = scaler_y.inverse_transform(wheat_yield_2023)
end_time = time.time()
times.append(end_time - start_time)

# Calculate the total wheat yield in tons
# Let user input the hectare
hectare = float(input("Enter the number of hectares: "))

wheat_yield = hectare * wheat_yield_2023[0][0]


print("\n\033[93m" + "Time Metrics" + "\033[0m")
print(f"Data Preparation: {times[0]:.4f}s")
print(f"Model Training: {times[1]:.4f}s")
print(f"Imputation: {times[2]:.4f}s")
print(f"Prediction: {times[3]:.4f}s")
print(f"Total time: {sum(times):.4f}s")

# Print the predicted wheat yield per hectare for 2023
print("\n\033[94m" + "Predictions for 2023" + "\033[0m")

print(f"Predicted {crop.split('_')[0]} yield ton per hectare for 2023: {wheat_yield_2023[0][0]}")
print(f"{crop.split('_')[0].title()} yield in tons: {wheat_yield}")

# Calculate the health score
health = calculateHealth(df_imputed, crop.split('_')[0], optimums)

# Print the health score
print("\n\033[92m" + "Health Score" + "\033[0m")
print(f"Health Score: {health['health_score'].tail(1).values[0]*100:.2f}%")