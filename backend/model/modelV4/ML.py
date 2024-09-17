# Imports
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from abc import ABC, abstractmethod

# This class defines a base (abstract) ML model that handles cleaning, feature engineering and training of the model without storing the data in the database. This ensures that the data can be easily changed (for example when improving the calculation of a feature).
# This class serves as a base class for ML models that will be tested against each other, and possible be ensembled to create a final model.
# The base class caters for feature engineering, handling missing values and training the model, but does not implement the training or prediction methods.
class ML(ABC):
    def __init__(self):
        self.historical_data = pd.read_csv('historical_data_cleaned.csv')
        self.yield_data = pd.read_csv('target.csv')

        # self.handle_missing_values()
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

        # Calculate the number of missing values per row
        missing_per_row = data_to_impute.isnull().sum(axis=1)

        # remove rows that are all NaN
        print(missing_per_row.value_counts().sort_index())
        data_to_impute = data_to_impute.dropna(how='all')
        missing_per_row = data_to_impute.isnull().sum(axis=1)
        print(missing_per_row.value_counts().sort_index())

        # Apply KNN Imputer
        imputer = KNNImputer(n_neighbors=5)
        imputed_data = data_to_impute.copy()
        imputed_data[:] = imputer.fit_transform(data_to_impute)

        # Combine the imputed data with the date column
        self.historical_data = pd.concat([date_column, imputed_data], axis=1)

        # Drop rows with missing values
        self.historical_data = self.historical_data.dropna()
        
         # Calculate the number of missing values per row
        # print("Distribution of missing values per row:")
        # missing_per_row = self.getMissingRowDistribution()
        
        # # Loop through the range of 1 to the number of columns
        # for n in range(1, self.historical_data.shape[1]):
        #     count = (missing_per_row == n).sum()  # Count rows with exactly n missing values
        #     print(f'Amount of rows missing {n} values: {count}')

        # Plot histogram of missing values per row
        counts, bins, patches = plt.hist(missing_per_row, bins=range(0, missing_per_row.max() + 1), edgecolor='black')

        # Add annotations above each bar
        for count, bin_edge in zip(counts, bins[:-1]):
            plt.text(bin_edge + 0.5, count, f'{int(count)}', ha='center', va='bottom')

        # plt.xlabel('Number of missing values')
        # plt.ylabel('Number of rows')
        # plt.title('Distribution of missing values per row')
        # plt.xticks(range(0, missing_per_row.max() + 1))  # Ensure x-ticks match bin edges
        # # plt.show()

        # Drop precipprob
        # self.historical_data = self.historical_data.drop(columns=['precipprob'])

        # Save as csv
        # self.historical_data.to_csv('historical_data_cleaned.csv', index=False)

    def getMissingRowDistribution(self):
        missing_per_row = self.historical_data.isnull().sum(axis=1)
        print(missing_per_row.value_counts().sort_index())

        return missing_per_row