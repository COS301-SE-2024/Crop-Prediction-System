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

class MultiScaleModel():
    def __init__(self, X, y):
        # super().__init__(X, y)
        self.X = X
        self.y = y

        self.X = {
            'pentadal': self.X,
            'weekly': self.X,
            'biweekly': self.X,
            'monthly': self.X,
            'quarterly': self.X,
            'yearly': self.X
        }
        self.y = {
            'pentadal': self.y,
            'weekly': self.y,
            'biweekly': self.y,
            'monthly': self.y,
            'quarterly': self.y,
            'yearly': self.y
        }

        self.modelRMSE = []
        self.modelPredictions = []
        self.actual = None

        self.models = []

        self.predX = {
            'pentadal': None,
            'weekly': None,
            'biweekly': None,
            'monthly': None,
            'quarterly': None,
            'yearly': None
        }

        self.prepare()
    
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

            # Drop X's yield column
            X = X.drop(columns=['yield'])

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
                # random_state=42,
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

            # Append the model
            self.models.append(best_model)

        return self.modelRMSE

    def predict(self):
        if len(self.models) == 0:
            return None

        predictions = []

        for i in range(len(self.models)):
            freq = list(self.X.keys())[i]

            # Predict
            y_pred = self.models[i].predict(self.predX[freq])
            predictions.append(y_pred)

            # Show predictions next to actual
            # plt.figure(figsize=(10, 6))
            # plt.plot(y_pred, label='Prediction', color='red', linestyle='dashed')
            # plt.plot(y, label='Actual', color='blue')
            # plt.xlabel('Index')
            # plt.ylabel('Value')
            # plt.title('Model Predictions vs Actual Values')
            # plt.legend()
            # plt.show()

        return predictions

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

        # Prepare self.X for each frequency
        for freq in self.X.keys():
            self.X[freq] = self.aggregate(freq, self.X)

        # For self.predX, select current date and 5 days ahead. Select the datasets of those dates
        for i in range(0,6):
            curr = datetime.datetime.now()
            curr += datetime.timedelta(days=i)
            for freq in self.X.keys():
                current_date = None

                if freq != 'yearly':
                    if freq == 'pentadal':
                        current_date = curr.timetuple().tm_yday // 5
                    elif freq == 'weekly':
                        current_date = curr.isocalendar().week
                    elif freq == 'biweekly':
                        current_date = curr.timetuple().tm_yday // 14
                    elif freq == 'monthly':
                        current_date = curr.month
                    elif freq == 'quarterly':
                        current_date = pd.to_datetime(curr).quarter
                    
                    if self.predX[freq] is None:
                        self.predX[freq] = self.X[freq][self.X[freq][freq] == current_date]
                    else:
                        self.predX[freq] = pd.concat([self.predX[freq], self.X[freq][self.X[freq][freq] == current_date]])
                else:
                    if self.predX[freq] is None:
                        self.predX[freq] = self.X[freq][self.X[freq][freq] == curr.year]
                    else:
                        self.predX[freq] = pd.concat([self.predX[freq], self.X[freq][self.X[freq][freq] == curr.year]])

        # Select only this year
        for freq in self.predX.keys():
            self.predX[freq] = self.predX[freq][self.predX[freq]["yearly"] == datetime.datetime.now().year]

        return self.X
    
    def aggregate(self, freq, data):
        # Cumulative or mean for each stage per year
        if (freq == 'yearly'):
            data[freq] = data[freq].groupby([freq]).agg({
                'tempmax': 'mean',
                'tempmin': 'mean',
                'dew_point': 'mean',
                'humidity': 'mean',
                'rain': 'sum',
                'pressure': 'mean',
                'clouds': 'mean',
                'uvi': 'mean',
                'tempmean': 'mean',
                'tempdiurnal': 'mean'
            }).reset_index()
        else:
            data[freq] = data[freq].groupby(["yearly", freq]).agg({
                'tempmax': 'mean',
                'tempmin': 'mean',
                'dew_point': 'mean',
                'humidity': 'mean',
                'rain': 'sum',
                'pressure': 'mean',
                'clouds': 'mean',
                'uvi': 'mean',
                'tempmean': 'mean',
                'tempdiurnal': 'mean'
            }).reset_index()

        return data[freq]


    def evaluate(self):
        pass

# if __name__ == '__main__':
#     msm = MultiScaleModel()

#     msm.prepare()
#     msm.train()