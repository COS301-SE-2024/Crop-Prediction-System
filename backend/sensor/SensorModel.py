import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

class SensorModel:
    def __init__(self):
        pass

    def train(self):
        # Import CSV
        data = pd.read_csv('backend/sensor/sensor_dataset.csv')

        # Rename weather_temperature to temperature
        data.rename(columns={'weather_temperature': 'temperature'}, inplace=True)

        # Rename weather_humidity to humidity
        data.rename(columns={'weather_humidity': 'humidity'}, inplace=True)

        X1 = data[['temperature', 'humidity']]
        y1 = data['soil_moisture']

        X2 = data[['temperature', 'humidity']]
        y2 = data['soil_temperature']

        X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=123)
        X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=123)

        xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators = 10, seed = 123, booster = 'gbtree')

        # Define the parameter grid
        param_dist = {
            'n_estimators': [100, 200, 300, 400, 500],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'max_depth': [3, 4, 5, 6, 7, 8],
            'min_child_weight': [1, 3, 5, 7],
            'gamma': [0, 0.1, 0.2, 0.3],
            'subsample': [0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
        }

        # Setup the random search with 3-fold cross-validation
        random_search_1 = RandomizedSearchCV(
            xgb_model,
            param_distributions=param_dist,
            n_iter=50,  # Number of parameter settings that are sampled
            scoring='neg_mean_squared_error',
            cv=3,  # 3-fold cross-validation
            verbose=1,
            n_jobs=-1,
            random_state=42,
        )

        # Setup the random search with 3-fold cross-validation
        random_search_2 = RandomizedSearchCV(
            xgb_model,
            param_distributions=param_dist,
            n_iter=50,  # Number of parameter settings that are sampled
            scoring='neg_mean_squared_error',
            cv=3,  # 3-fold cross-validation
            verbose=1,
            n_jobs=-1,
            random_state=42,
        )

        # Fit the model
        random_search_1.fit(X1_train, y1_train)
        random_search_2.fit(X2_train, y2_train)

        # Best model based on the best parameters
        best_model_1 = random_search_1.best_estimator_
        best_model_2 = random_search_2.best_estimator_

        # Make predictions with the best model
        y1_pred = best_model_1.predict(X1_test)
        y2_pred = best_model_2.predict(X2_test)

        mse1 = mean_squared_error(y1_test, y1_pred)
        rmse1 = np.sqrt(mse1)

        mse2 = mean_squared_error(y2_test, y2_pred)
        rmse2 = np.sqrt(mse2)

        print("RMSE 1: ", rmse1)
        print("RMSE 2: ", rmse2)

        # Plot predictions (actual vs predicted)
        plt.figure(figsize=(12, 6))
        plt.plot(y1_test.values, label='Actual soil moisture')
        plt.plot(y1_pred, label='Predicted soil moisture', linestyle='dashed')
        plt.plot(y2_test.values, label='Actual soil temperature')
        plt.plot(y2_pred, label='Predicted soil temperature', linestyle='dashed')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Model Predictions vs Actual Values')
        plt.legend()
        plt.show()

        # Save models
        best_model_1.save_model('backend/sensor/soil_moisture_model.json')
        best_model_2.save_model('backend/sensor/soil_temperature_model.json')

        return rmse1, rmse2

    def predict(self, temperature, humidity):
        # Load models
        model_1 = xgb.XGBRegressor()
        model_1.load_model('backend/sensor/soil_moisture_model.json')

        model_2 = xgb.XGBRegressor()
        model_2.load_model('backend/sensor/soil_temperature_model.json')

        X = pd.DataFrame([[temperature, humidity]], columns=['temperature', 'humidity'])

        # Predict soil moisture
        y1_pred = model_1.predict(X)

        # Predict soil temperature
        y2_pred = model_2.predict(X)

        return y1_pred, y2_pred

# if __name__ == '__main__':
#     model = SensorModel()
#     # model.train()
#     print(model.predict(25, 50))