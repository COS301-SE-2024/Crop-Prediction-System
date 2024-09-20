import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np

class SensorModel:
    def __init__(self):
        pass

    def train(self):
        # Load the data
        data = pd.read_csv('NPK_dataset.csv')

        # Encode the categorical label (crop type)
        le = LabelEncoder()
        data['label'] = le.fit_transform(data['label'])

        # Split the data into features (X) and targets (y for N, P, K)
        X = data[['temperature', 'humidity', 'ph', 'rainfall', 'label']]

        # Independent target variables
        y_N = data['N']
        y_P = data['P']
        y_K = data['K']

        # Split into train and test sets
        X_train, X_test, y_N_train, y_N_test = train_test_split(X, y_N, test_size=0.2, random_state=42)
        X_train, X_test, y_P_train, y_P_test = train_test_split(X, y_P, test_size=0.2, random_state=42)
        X_train, X_test, y_K_train, y_K_test = train_test_split(X, y_K, test_size=0.2, random_state=42)

        # Define and train separate XGBoost models for N, P, and K
        model_N = xgb.XGBRegressor(objective ='reg:squarederror', random_state=42)
        model_P = xgb.XGBRegressor(objective ='reg:squarederror', random_state=42)
        model_K = xgb.XGBRegressor(objective ='reg:squarederror', random_state=42)

        model_N.fit(X_train, y_N_train)
        model_P.fit(X_train, y_P_train)
        model_K.fit(X_train, y_K_train)

    def predict(self, temperature, humidity, ph, rainfall, crop):
        if (crop not in ['rice', 'wheat', 'maize', 'lentil', 'jute', 'coffee', 'cotton', 'sugarcane', 'tobacco', 'pepper', 'apple', 'banana', 'mango', 'grapes']):
            return 'Invalid crop type'

        # Load the model
        model = xgb.XGBRegressor()
        model.load_model('NPK_model.json')

        # Encode the crop type
        le = LabelEncoder()
        crop = le.transform([crop])

        # Predict the N, P, and K values
        prediction = model.predict([[temperature, humidity, ph, rainfall, crop]])
        return prediction