import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Function to create LSTM model
def create_lstm_model(seq_length, input_shape):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# Function to create ensemble of LSTM models
def create_lstm_ensemble(num_models, seq_length, input_shape):
    models = []
    for _ in range(num_models):
        model = create_lstm_model(seq_length, input_shape)
        models.append(model)
    return models

# Import CSV data
data = pd.read_csv('processed_data/uea_analysed.csv')

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Separate features and target variable
X = df.drop(columns=['date', 'wheat_ton_per_hectare'])
y = df['wheat_ton_per_hectare']

# Normalize the data
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_weighted = scaler_X.fit_transform(X)
y_weighted = scaler_y.fit_transform(y.values.reshape(-1, 1))

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

# Define parameters for ensemble
num_models = 3  # Number of LSTM models in the ensemble

# Create ensemble of LSTM models
models = create_lstm_ensemble(num_models, seq_length, (seq_length, X_train.shape[2]))

# Train each model in the ensemble
epoch = [100, 150, 200]
batch = [50, 40, 30]
histories = []
for i, model in enumerate(models):
    print(f"Training model {i+1}/{num_models}")
    history = model.fit(X_train, y_train, epochs=epoch[i], validation_split=0.2, batch_size=batch[i])
    histories.append(history)

# Evaluate each model in the ensemble
ensemble_preds = []
for model in models:
    y_pred = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred)
    ensemble_preds.append(y_pred)

# Average predictions from ensemble
avg_pred = np.mean(ensemble_preds, axis=0)

# Evaluate ensemble performance
mse_ensemble = mean_squared_error(scaler_y.inverse_transform(y_test), avg_pred)
r2_ensemble = r2_score(scaler_y.inverse_transform(y_test), avg_pred)

# Evaluate each model in the ensemble
mse = [mean_squared_error(scaler_y.inverse_transform(y_test), pred) for pred in ensemble_preds]
r2 = [r2_score(scaler_y.inverse_transform(y_test), pred) for pred in ensemble_preds]

# Print ensemble performance
print(f"Ensemble Mean Squared Error: {mse_ensemble}")
print(f"Ensemble R-squared: {r2_ensemble}")

# Print performance of each model in the ensemble
for i in range(num_models):
    print(f"Model {i+1} Mean Squared Error: {mse[i]}")
    print(f"Model {i+1} R-squared: {r2[i]}")

# Pick the best model in the ensemble
best_model_index = np.argmin([history.history['val_loss'][-1] for history in histories])

# Save the best model
model = models[best_model_index]

print(f"Ensemble Mean Squared Error: {mse}")
print(f"Ensemble R-squared: {r2}")

# Sample data for 2023
norm_dataset = pd.read_csv('processed_data/uea_converted.csv')
norm_gdd = pd.read_csv('processed_data/growing_season.csv')

# Get the max and min values of each feature
max_values = norm_dataset.max()
min_values = norm_dataset.min()
gdd_max = norm_gdd['gdd'].max()
gdd_min = norm_gdd['gdd'].min()

# Sample data for 2023
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

# Convert the input data for 2023 to a DataFrame
X_2023 = pd.DataFrame([data_2023])

# Ensure the input data for 2023 has the correct sequence length
X_2023_seq = []
for i in range(seq_length):
    X_2023_seq.append(X_2023.values.flatten())
X_2023_seq = np.array(X_2023_seq).reshape((1, seq_length, X_2023.shape[1]))

# Reshape the data for the LSTM model
X_2023_seq = scaler_X.transform(X_2023_seq.reshape(-1, X_2023.shape[1]))
X_2023_seq = X_2023_seq.reshape((1, seq_length, X_2023.shape[1]))

# Predict the wheat yield for 2023
wheat_yield_2023 = model.predict(X_2023_seq)
wheat_yield_2023 = scaler_y.inverse_transform(wheat_yield_2023)

# Print the predicted wheat yield per hectare for 2023
print(f"Predicted wheat yield per hectare for 2023: {wheat_yield_2023[0][0]}")

# Calculate the total wheat yield in tons
hectare = 537950
wheat_yield = hectare * wheat_yield_2023[0][0]
print(f"Wheat yield in tons: {wheat_yield}")

# Show feature importance
importance = model.layers[0].get_weights()[0]
feature_importance = np.mean(importance, axis=1)

features = ['potential_evapotranspiration', 'cloud_cover', 'precipitation', 'maximum_temperature', 'rain_days', 'minimum_temperature', 'vapour_pressure', 'ground_frost_frequency', 'diurnal_temperature_range', 'mean_temperature', 'gdd']

plt.bar(features, feature_importance)
plt.xticks(rotation=45)
plt.ylabel('Feature Importance')
plt.title('Feature Importance for Wheat Yield Prediction')
plt.show()

# Save the model
model.save('wheat_yield_prediction_model.keras')
print("Model saved successfully")
