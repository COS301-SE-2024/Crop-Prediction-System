# Imports
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from abc import ABC, abstractmethod

# This class defines a base (abstract) ML model that handles cleaning, feature engineering and training of the model without storing the data in the database. This ensures that the data can be easily changed (for example when improving the calculation of a feature).
# This class serves as a base class for ML models that will be tested against each other, and possible be ensembled to create a final model.
# The base class caters for feature engineering, handling missing values and training the model, but does not implement the training or prediction methods.
class ML(ABC):
    def __init__(self, X, y):
        self.historical_data = X
        self.yield_data = y

        self.handle_missing_values()
        self.handle_missing_target_values()
        self.feature_engineering()

    @abstractmethod
    def train(self):
        pass
    
    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def prepare(self):
        pass

    def feature_engineering(self):
        # self.historical_data['rain_days'] = self.historical_data['rain'] > 0
        pass

    def handle_missing_target_values(self):
        # remove rows where yield is NaN
        self.yield_data = self.yield_data.dropna(subset=['yield'])

    def handle_missing_values(self):
        date_column = self.historical_data['date']
        data_to_impute = self.historical_data.drop(columns=['date'])

        # remove rows that are all NaN
        data_to_impute = data_to_impute.dropna(how='all')

        # Apply KNN Imputer
        imputer = KNNImputer(n_neighbors=5)
        imputed_data = data_to_impute.copy()
        imputed_data[:] = imputer.fit_transform(data_to_impute)

        # Combine the imputed data with the date column
        self.historical_data = pd.concat([date_column, imputed_data], axis=1)

        # Drop rows with missing values
        self.historical_data = self.historical_data.dropna()