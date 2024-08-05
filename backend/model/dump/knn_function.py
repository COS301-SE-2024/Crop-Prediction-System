import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from alive_progress import alive_bar

def knn_impute(dframe):
    print("Imputing missing values using KNN...")

    df = dframe.copy()

    # Drop columns that end with "_ton_per_hectare"
    df = df.drop(columns=df.filter(regex='_ton_per_hectare').columns)

    # Save for later
    ton_per_hectare = dframe.filter(regex='_ton_per_hectare')

    # Drop date column
    df = df.drop(columns=['date'])

    # Check for missing values
    missing_values = df.isnull().sum()

    # Sort columns by the number of missing values
    missing_values = missing_values[missing_values > 0].sort_values()

    # Iteratively impute missing values for each column
    with alive_bar(missing_values.size) as bar:
        for column in missing_values.index:
            # print(f"Filling missing values for column: {column}")

            # print(f"X shape: {df.shape}")
            # Prepare X (features without missing values) and y (target column)
            # Drop rows with missing values
            X = df[df[column].notnull()]
            y = df[column].dropna()
            
            # print(f"X shape: {X.shape}, y shape: {y.shape}")
            # print(f"X head: {X.head()}")
            
            # Normalize the data
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)

            # Initialize KNN model
            knn_model = KNeighborsRegressor(n_neighbors=5, weights='distance')

            # Fit the model
            knn_model.fit(X_scaled, y)

            # Predict missing values
            imputed_values = knn_model.predict(X_scaled)

            # print(f"Imputed values: {imputed_values}")

            # Update the dataframe with imputed values
            # print(f"Original column: {df[column]}")
            # print(f"Imputed values: {imputed_values}")
            # print(df[column].isnull())
            # print(df.loc[df[column].isnull(), column])
            indexOfMissing = df.loc[df[column].isnull(), column].index-1
            df.loc[df[column].isnull(), column] = imputed_values[indexOfMissing]
            bar()
    
    # Re-add the "ton_per_hectare" columns
    df = pd.concat([df, ton_per_hectare], axis=1)

    # Green
    print("\033[92m" + "Imputation complete" + "\033[0m")
    print(df.tail())
    return df
