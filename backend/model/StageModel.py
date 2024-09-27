import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from backend.definitions.crop import Crop
import datetime

# XGBoost
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import numpy as np

# * Stage Model Information
# This model builds on the previously deployed model by grouping data into crop growing stages (sowing, tillering, heading, etc.) and then predicts the sequence in the given timeframe.

# Known disadvantages: cumulative variables are low at the start of a stage, causing concerningly low predictions from a farmer's perspective. 
    # * (Fixed this by adding a day to date for the current stage)

class StageModel():
    def __init__(self, X, y, crop : Crop):
        self.X = X
        self.y = y

        self.crop = crop
        self.current_stage = None

        self.model = None

        # self.predX = None

        self.prepare()

    def train(self):
        # If not in stage, do not train
        if self.X["stage"].isnull().all():
            return None

        self.X = self.X.drop(['stage'], axis=1)

        # Split into training and testing data
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2)

        xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators = 10, booster = 'gbtree')

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
            n_iter=1,  # Number of parameter settings that are sampled
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

        # print("RMSE: ", rmse)
        # print(y_pred)

        # Make predictions on the entire dataset
        # y_pred = best_model.predict(self.X)

        self.model = best_model

        # Plot the prediction
        # plt.figure(figsize=(10, 6))
        # plt.plot(y_pred, label='Prediction', color='red', linestyle='dashed')
        # plt.plot(self.y.values, label='Actual', color='blue')
        # plt.xlabel('Index')
        # plt.ylabel('Value')
        # plt.title('Model Predictions vs Actual Values')
        # plt.legend()
        # plt.show()

        return rmse


    def predict(self):
        # Predict on the current year
        return self.model.predict(self.X.tail(1))

    def prepare(self):
        # Sort crop stages by day
        self.crop.stages = dict(sorted(self.crop.stages.items(), key=lambda item: item[1]["day"]))

        # get current stage of the crop
        today = date.today()
        day_of_year = today.timetuple().tm_yday

        # Get current stage
        for s_name, s_info in self.crop.stages.items():
            if day_of_year >= s_info["day"]:
                self.current_stage = s_name
            else:
                break
        
        # Group data into stages
        # First add a stage variable
        self.X["stage"] = None

        # Convert date to time
        self.X["date"] = pd.to_datetime(self.X["date"])

        self.X["day"] = self.X["date"].apply(lambda x: x.timetuple().tm_yday)
        self.X["year"] = self.X["date"].apply(lambda x: x.year)

        # Group each stage
        for s_name, s_info in self.crop.stages.items():
            self.X.loc[(self.X['day'] >= s_info["day"]), 'stage'] = s_name

        self.X = self.X[self.X["stage"].notnull()]

        # # Prediction date is current date + 5 days
        # self.predX = self.X[self.X["day"] >= day_of_year]

        # # Select only data from this year
        # self.predX = self.predX[self.predX["year"] == today.year]

        # # In predX, drop date, day, pentadal, weekly, biweekly, monthly, quarterly, stage, year
        # self.predX.drop(['date', 'day', 'stage'], axis=1, inplace=True)

        # Remove data > day of year
        self.X = self.X[self.X["day"] <= day_of_year]

        # Cumulative or mean for each stage per year
        self.X = self.X.groupby(["year", "stage"]).agg({
            'tempmax': 'mean',
            'tempmin': 'mean',
            'dew_point': 'mean',
            'humidity': 'mean',
            'rain': 'sum',
            'pressure': 'mean',
            'clouds': 'mean',
            'uvi': 'mean',
            'tempmean': 'mean',
            'tempdiurnal': 'mean',
            'soil_moisture': 'mean',
            'soil_temperature': 'mean'
        }).reset_index()

        # Select only current stage
        self.X = self.X[self.X["stage"] == self.current_stage]

        # Replace outliers with mean
        for col in self.X.columns:
            if self.X[col].dtype == 'float64':
                self.X[col] = self.X[col].apply(lambda x: self.X[col].mean() if x < self.X[col].mean() - 3 * self.X[col].std() or x > self.X[col].mean() + 3 * self.X[col].std() else x)

        # Merge with yield data
        self.X = pd.merge(self.X, self.y, on='year', how='inner')

        self.y = self.X["yield"]
    
        # Drop yield column
        self.X.drop('yield', axis=1, inplace=True)

    def evaluate(self):
        pass

# if __name__ == '__main__':
#     # Define some crop
#     c = Crop(
#         name="wheat",
#         t_base=5.0, 
#         stages={
#             "sowing": {"day": 111},
#             "germination": {"day": 151},
#             "tillering": {"day": 182},
#             "heading": {"day": 243},
#             "maturity": {"day": 304}
#         }
#     )

#     sm = StageModel(c)

#     sm.prepare()
#     sm.train()