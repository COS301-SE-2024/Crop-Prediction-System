import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

# Import the dataset
data = pd.read_csv('processed_data/model_data.csv')

# Convert the data to a DataFrame (this step is not necessary if 'data' is already a DataFrame)
df = pd.DataFrame(data)

# print(df.columns)
# print(df)

# Ignore "maize_ton_per_hectare","maize_comm_ton_per_hectare","maize_non_comm_ton_per_hectare","wheat_ton_per_hectare","groundnuts_ton_per_hectare","sunflowerseed_ton_per_hectare","sorghum_ton_per_hectare","soybeans_ton_per_hectare","barley_ton_per_hectare","canola_ton_per_hectare","oats_ton_per_hectare"
df = df.drop(columns=['date', 'maize_ton_per_hectare', 'maize_comm_ton_per_hectare', 'maize_non_comm_ton_per_hectare', 'wheat_ton_per_hectare', 'groundnuts_ton_per_hectare', 
'sunflowerseed_ton_per_hectare', 'sorghum_ton_per_hectare', 'soybeans_ton_per_hectare', 'barley_ton_per_hectare', 'canola_ton_per_hectare', 'oats_ton_per_hectare'])

# Drop gdd
df = df.drop(columns=['gdd'])

# Check for missing values
missing_values = df.isnull().sum()

# Sort the columns by the number of missing values
missing_values = missing_values.sort_values(ascending=True)

# Drop rows in missing_values that have no missing values
missing_values = missing_values[missing_values > 0]
# print(f"Columns with missing values: {missing_values}")

# Select all entries with columns that are complete
complete_columns = df.columns[df.notnull().all()].tolist()
# print(f"Columns with no missing values: {complete_columns}")

# print("Trimmed")
# print(dfResult)

def rec_knn(missing_values, df):
    column = missing_values.index[0]
    print(f"Filling missing values for column: {column}")
    
    X = df.drop(missing_values.index, axis=1)
    y = df[column]

    # Select all rows where the target column is not null
    X = X[y.notnull()]
    y = y[y.notnull()]

    # Normalize the data
    scaler = MinMaxScaler()

    # Fit the scaler on the data
    X_scaled = scaler.fit_transform(X)

    print(X_scaled)

    # Initialize KNN model
    knn_model = KNeighborsRegressor(n_neighbors=5, weights='distance')

    # Fit the model
    knn_model.fit(X_scaled, y)

    # Predict missing values
    imputed_values = knn_model.predict(X_scaled)

    # Make sure imputed_values is the same length as the original data
    imputed_values = np.concatenate([imputed_values, np.full(missing_values[column], np.nan)])

    # Replace missing values with imputed values
    df.loc[df[column].isnull(), column] = imputed_values[df[column].isnull()]

    print(df[column])

    # Update the missing_values
    missing_values = df.isnull().sum()

    # Drop the column from missing_values
    missing_values = missing_values[missing_values > 0]

    # Sort the columns by the number of missing values
    missing_values = missing_values.sort_values(ascending=True)

    if missing_values.empty:
        print("\033[92m" + "All missing values have been filled!" + "\033[0m")
    else:
        print("\033[92m" + f"Next column to fill: {missing_values.index[0]}" + "\033[0m")

    print(f"Missing values left: {missing_values}")
    print(f"Current DF shape: {df.shape}")

    if missing_values.empty:
        return df, knn_model
    else:
        return rec_knn(missing_values, df)
    
dfResult, knn_model = rec_knn(missing_values, df)

# Re-add the date column
date = data['date']

# Concatenate the date column with the imputed data
dfResult = pd.concat([date, dfResult], axis=1)

# Now calculate the soil moisture %
# First calculate combined effect of precipitation and evapotranspiration for the next 16 days
# dfResult['z_k'] = dfResult['precipitation'] / dfResult['potential_evapotranspiration']

# # Calculate the soil moisture by taking the average of the combined effect of precipitation and evapotranspiration for the next 1 entry
# dfResult['soil_moisture'] = dfResult['z_k'].rolling(window=1).mean()

# # Apply a constant factor and take the inverse of the soil moisture to get the soil moisture %
# dfResult['soil_moisture'] = 1 - 1 / (dfResult['soil_moisture'] ** 0.74)

# Re-add "maize_ton_per_hectare","maize_comm_ton_per_hectare","maize_non_comm_ton_per_hectare","wheat_ton_per_hectare","groundnuts_ton_per_hectare","sunflowerseed_ton_per_hectare","sorghum_ton_per_hectare","soybeans_ton_per_hectare","barley_ton_per_hectare","canola_ton_per_hectare","oats_ton_per_hectare"
yield_data = data[['maize_ton_per_hectare', 'maize_comm_ton_per_hectare', 'maize_non_comm_ton_per_hectare', 'wheat_ton_per_hectare', 'groundnuts_ton_per_hectare', 'sunflowerseed_ton_per_hectare', 'sorghum_ton_per_hectare', 'soybeans_ton_per_hectare', 'barley_ton_per_hectare', 'canola_ton_per_hectare', 'oats_ton_per_hectare']]

dfResult = pd.concat([dfResult, yield_data], axis=1)

# Save the imputed data to a CSV file
dfResult.to_csv('processed_data/model_data_imputed_v2.csv', index=False)

# Save model to be reused when there are new data with missing values
import joblib
joblib.dump(knn_model, 'missingValues.joblib')

print("Data imputation complete!")