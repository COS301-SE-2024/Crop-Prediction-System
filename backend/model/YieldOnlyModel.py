# XGBoost
from sklearn.model_selection import train_test_split
import xgboost as xgb

# ARIMA
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.metrics import mean_squared_error

# Plotting
import matplotlib.pyplot as plt

# Datetime
from datetime import datetime

# * Yield Only Model Information
# This model aims to predict yield purely by means of historic yield data, and doesn't take into account any weather or crop-specific data. The aim of this model is for pure evaluation and prevention of inaccurate predictions. The fusion model will use the confidence level of the Yield Only Model to determine if other model predictions in the ensemble were sound or not.

# Also, the Yield Only Model will perform ensemble predictions within itself to determine the confidence level of its predictions.

class YieldOnlyModel():
    def __init__(self, X):
        # super().__init__(X, y)
        self.X = X

        self.model = None

        self.prepare()

    def train(self):
        # Split data
        X_train = self.X
        X_test = self.X

        # # ====================
        # # ARIMA MODEL
        # # ====================
        # # Train ARIMA on the 'yield' column (univariate)
        # arima_model = ARIMA(X_train['yield'], order=(5,1,0))
        
        # # Fit model
        # arima_model_fit = arima_model.fit()
        
        # # Forecast using ARIMA
        # arima_predictions = arima_model_fit.forecast(steps=len(X_test))
        
        # # Calculate ARIMA RMSE
        # arima_rmse = np.sqrt(mean_squared_error(X_test['yield'], arima_predictions))

        # ====================
        # XGBOOST MODEL
        # ====================
        xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.1,
            n_jobs=-1,
            # random_state=42,
        )
        
        # Fit XGBoost on all features except 'yield'
        xgb_model.fit(X_train.drop(columns=['yield']), X_train['yield'])
        
        # Predict using XGBoost
        xgb_predictions = xgb_model.predict(X_test.drop(columns=['yield']))

        # ====================
        # ENSEMBLE MODEL
        # ====================
        # Pick the best model based on RMSE
        # if arima_rmse < xgb_rmse:
        #     best_model = arima_model_fit
        #     best_predictions = arima_predictions
        # else:
        best_model = xgb_model
        best_predictions = xgb_predictions
        
        # Calculate Ensemble RMSE
        rmse = np.sqrt(mean_squared_error(X_test['yield'], best_predictions))

        # ====================
        # PRINT RESULTS
        # ====================
        # print(f"ARIMA RMSE: {arima_rmse}")
        # print(f"XGBoost RMSE: {xgb_rmse}")
        # print(f"Ensemble RMSE: {best_rmse}")

        self.model = best_model

        return rmse


    def predict(self):
        # Predict into the future
        future_X = self.X.copy()
        future_X['year'] = future_X['year'] + 1
        future_X = future_X.drop(columns=['yield'])

        # Predict using the best model
        predictions = self.model.predict(future_X)

        # # plot the predictions
        # plt.plot(self.X['year'], self.X['yield'], label='Historical Yield')
        # plt.plot(future_X['year'], predictions, label='Future Yield', color='red', linestyle='dashed')
        # plt.xlabel('Year')
        # plt.ylabel('Yield')
        # plt.title('Yield Prediction')
        # plt.legend()
        # plt.show()

        return predictions

    def prepare(self):
        # Drop na
        self.X = self.X.dropna()

        # Drop outliers
        self.X = self.X[(self.X['yield'] < (self.X['yield'].mean() + 3 * self.X['yield'].std())) & (self.X['yield'] > (self.X['yield'].mean() - 3 * self.X['yield'].std()))]

        # Reset index
        self.X = self.X.reset_index(drop=True)

    def evaluate(self):
        pass

# if __name__ == '__main__':
#     yom = YieldOnlyModel()
#     yom.prepare()
#     yom.train()