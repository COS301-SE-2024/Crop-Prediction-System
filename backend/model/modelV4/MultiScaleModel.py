from ML import ML
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt

# XGBoost
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# * Multi-Scale Model Information
# This model aims to experiment with the same data on different frequencies (i.e. daily, monthly, yearly) and then let the models act as an ensemble model by taking the average output between n models.

class MultiScaleModel(ML):
    def __init__(self):
        ML.__init__(self)

        self.X = {
            'pentadal': self.historical_data,
            'weekly': self.historical_data,
            'biweekly': self.historical_data,
            'monthly': self.historical_data,
            'quarterly': self.historical_data,
            'yearly': self.historical_data
        }
        self.y = {
            'pentadal': self.yield_data,
            'weekly': self.yield_data,
            'biweekly': self.yield_data,
            'monthly': self.yield_data,
            'quarterly': self.yield_data,
            'yearly': self.yield_data
        }

        self.modelRMSE = []
        self.modelPredictions = []
        self.actual = None
    
    def train(self):
        # Traverse through each frequency, pick ones where a certain variable is the same (i.e. year)
        for freq in self.X.keys():
            X = self.X[freq]
            y = self.y[freq]

            # Rename y's yearly column to match X's yearly column
            y = y.rename(columns={'year': 'yearly'})
            
            # Get current date
            current_date = datetime.datetime.now()

            # Get current pentadal
            if freq != 'yearly':
                if freq == 'pentadal':
                    current_date = current_date.timetuple().tm_yday // 5
                elif freq == 'weekly':
                    current_date = current_date.isocalendar().week
                elif freq == 'biweekly':
                    current_date = current_date.timetuple().tm_yday // 14
                elif freq == 'monthly':
                    current_date = current_date.month
                elif freq == 'quarterly':
                    current_date = pd.to_datetime(current_date).quarter
                
                X = X[X[freq] == current_date]
            else:
                pass

            # Merge X and y on year (X yearly and y year)
            X = pd.merge(X, y, on='yearly', how='inner')
            y = X["yield"]

            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

            # Drop na values
            X_train = X_train.dropna()
            y_train = y_train.dropna()

            # XGBoost model
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
            random_search = RandomizedSearchCV(
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
            random_search.fit(X_train, y_train)

            # Best model based on the best parameters
            best_model = random_search.best_estimator_

            # Make predictions with the best model
            y_pred = best_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)

            self.modelRMSE.append(rmse)

            # Make predictions on the entire dataset
            y_pred = best_model.predict(X)
            self.modelPredictions.append(y_pred)
            self.actual = y

        # Plot the prediction
        print(self.modelRMSE)

        # Plot the prediction
        plt.plot(self.modelPredictions[0], label='Pentadal')
        plt.plot(self.modelPredictions[1], label='Weekly')
        plt.plot(self.modelPredictions[2], label='Biweekly')
        plt.plot(self.modelPredictions[3], label='Monthly')
        plt.plot(self.modelPredictions[4], label='Quarterly')
        plt.plot(self.modelPredictions[5], label='Yearly')
        plt.plot(self.actual, label='Actual')
        plt.legend()
        plt.show()

    def predict(self, data):
        pass

    def prepare(self):
        # Convert all to date
        for freq in self.X.keys():
            self.X[freq]["date"] = pd.to_datetime(self.X[freq]["date"])

            # Add year by default (lowest frequency)
            self.X[freq]["yearly"] = self.X[freq]["date"].apply(lambda x: x.year)

            # Add day of year
            self.X[freq]["day"] = self.X[freq]["date"].apply(lambda x: x.timetuple().tm_yday)

        # Add pentadal counter
        for freq in self.X.keys():
            if freq == 'pentadal':
                self.X[freq]["pentadal"] = self.X[freq]["day"].apply(lambda x: x // 5)
            elif freq == 'weekly':
                self.X[freq]["weekly"] = self.X[freq]["date"].apply(lambda x: x.week)
            elif freq == 'biweekly':
                self.X[freq]["biweekly"] = self.X[freq]["day"].apply(lambda x: x // 14)
            elif freq == 'monthly':
                self.X[freq]["monthly"] = self.X[freq]["date"].apply(lambda x: x.month)
            elif freq == 'quarterly':
                self.X[freq]["quarterly"] = self.X[freq]["date"].apply(lambda x: x.quarter)
            elif freq == 'yearly':
                pass

        # Prepare data for each frequency
        for freq in self.X.keys():
            self.aggregate(freq)
    
    def aggregate(self, freq):
        # Cumulative or mean for each stage per year
        if (freq == 'yearly'):
            self.X[freq] = self.X[freq].groupby([freq]).agg({
                'tempmax': 'mean',
                'tempmin': 'mean',
                'dew_point': 'mean',
                'humidity': 'mean',
                'rain': 'sum',
                'pressure': 'mean',
                'clouds': 'mean',
                'solarradiation': 'mean',
                'solarenergy': 'sum',
                'uvi': 'mean',
                'tempmean': 'mean',
                'tempdiurnal': 'mean'
            }).reset_index()
        else:
            self.X[freq] = self.X[freq].groupby(["yearly", freq]).agg({
                'tempmax': 'mean',
                'tempmin': 'mean',
                'dew_point': 'mean',
                'humidity': 'mean',
                'rain': 'sum',
                'pressure': 'mean',
                'clouds': 'mean',
                'solarradiation': 'mean',
                'solarenergy': 'sum',
                'uvi': 'mean',
                'tempmean': 'mean',
                'tempdiurnal': 'mean'
            }).reset_index()


    def evaluate(self):
        pass

if __name__ == '__main__':
    msm = MultiScaleModel()

    msm.prepare()
    msm.train()