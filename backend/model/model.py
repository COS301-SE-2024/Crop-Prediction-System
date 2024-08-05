# Defines the base model for crop prediction that predicts yield
from pydantic import BaseModel
# from definitions import Crop

# Model specific imports
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import datetime

# Supabase imports
from supabase import create_client, Client
from dotenv import load_dotenv
import os

from pydantic import BaseModel, Field
from typing import Dict, List

class Crop(BaseModel):
    name: str = Field(..., description="Name of the crop.")
    t_base: float = Field(..., description="Base temperature for the crop.")
    stages: Dict[str, Dict[str, float]] = Field(
        ..., description="Associative 3D array for crop growth stages."
    )

class supabaseInstance:
    __instance = None # private instance variable

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get Supabase URL and Key
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")

        # Create Supabase client
        self.sbClient: Client = create_client(self.url, self.key)

    def get_client(self):
        if not supabaseInstance.__instance:
            supabaseInstance.__instance = supabaseInstance()

        return supabaseInstance.__instance.sbClient

class Model:
    def __init__(self, c : Crop, sb : supabaseInstance):
        self.crop = c
        self.sb = sb

    # Load data
    def load_data(self, field_id = None):
        try:
            model_data = self.load_model_data(field_id)
            if "error" in model_data:
                return model_data  # Return the error message if data loading failed
            
            print("Model Data:")
            print(model_data)  # Debug: Print the first few rows of model_data

            historical_data = self.load_yields()
            if "error" in historical_data:
                return historical_data  # Return the error message if data loading failed

            print("Historical Data:")
            print(historical_data)  # Debug: Print the first few rows of historical_data

            # Merge data and historical_data on the 'year' column
            data = pd.merge(model_data, historical_data, on='year', how='left')
            print("Merged Data:")
            print(data.head())  # Debug: Print the first few rows of the merged data

            return data
        except Exception as e:
            return {"error": f"An error occurred while loading data: {str(e)}"}
        
    def load_model_data(self, field_id = None):
        dict = {"fieldid": field_id} if field_id else {}
        response = self.sb.rpc('get_model_data', dict).execute()
        if response.data == []:
            return {"error": "Data not found. Field ID may be invalid or may not have any data."}
        
        model_data = pd.DataFrame(response.data)

        return model_data
        
    def load_yields(self):
        cropClass = self.crop.name + "_ton_per_hectare"
        dict = {"crop": cropClass}
        
        # Execute RPC call
        response = self.sb.rpc('get_historical_yields', dict).execute()
        
        # Check if data is returned
        if not response.data:
            return {"error": "Data not found. Crop name may be invalid or may not have any data."}
        
        # Convert response data to DataFrame
        historical_data = pd.DataFrame(response.data)
        
        # Ensure 'production_year' column exists
        if 'production_year' not in historical_data.columns:
            return {"error": "'production_year' column not found in data."}
        
        # Adjust 'year' based on 'production_year'
        historical_data['year'] = historical_data['production_year'].str[0:4].astype(int) + 1
        
        # Drop 'production_year' column
        historical_data.drop('production_year', axis=1, inplace=True)
        
        # Return the cleaned DataFrame
        return historical_data


    # Train
    def train(self, data):
        # Assuming 'day' represents the day of the year
        today = datetime.datetime.now()
        day_of_year = today.timetuple().tm_yday

        xgbins = [stage['day'] for stage in self.crop.stages.values()]
        # append the last day of the year
        xgbins.append(365)

        # Determine the current stage
        current_stage = pd.cut([day_of_year], bins=xgbins, labels=self.crop.stages.keys())[0]

        # Filter data based on the current stage
        stage_data = data[data['stage'] == current_stage]

        X = stage_data.drop(['year', 'stage', 'yield', 'field_id', 'id'], axis=1)
        y = stage_data['yield']

        # Define the XGBoost model
        xgb_model = xgb.XGBRegressor(objective='reg:squarederror')

        # Define the parameter grid
        param_dist = {
            'n_estimators': [100, 200, 300, 400, 500],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'max_depth': [3, 4, 5, 6, 7, 8],
            'min_child_weight': [1, 3, 5, 7],
            'gamma': [0, 0.1, 0.2, 0.3],
            'subsample': [0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
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
            random_state=42
        )

        # Fit the random search model
        random_search.fit(X, y)

        # Best model based on the best parameters
        best_model = random_search.best_estimator_

        # Make predictions with the best model
        y_pred = best_model.predict(X)
        mse = mean_squared_error(y, y_pred)

        # Save the model
        self.save(best_model)

    # Predict
    def predict(self, data):
        # Load the model
        model = xgb.Booster()
        model.load_model('model.json')

        # Convert data to a DMatrix
        dmatrix = xgb.DMatrix(data)

        # Make predictions
        predictions = model.predict(dmatrix)

        return predictions

    # Evaluate
    def evaluate(self):
        # Load the model
        model = xgb.Booster()
        model.load_model('model.json')

        # Load the data
        data = self.load_data()

        today = datetime.datetime.now() 
        day_of_year = today.timetuple().tm_yday

        xgbins = [stage['day'] for stage in self.crop.stages.values()]
        # append the last day of the year
        xgbins.append(365)

        # Determine the current stage
        current_stage = pd.cut([day_of_year], bins=xgbins, labels=self.crop.stages.keys())[0]

        print(f"Current stage: {current_stage}")

        # Filter data based on the current stage
        stage_data = data[data['stage'] == current_stage]

        X = stage_data.drop(['year', 'stage', 'yield', 'field_id', 'id'], axis=1)
        y_true = stage_data['yield']  # Assuming 'yield' is the actual target value you want to compare against

        # Convert X to a DMatrix
        dmatrix = xgb.DMatrix(X)

        # Make predictions
        predictions = model.predict(dmatrix)

        # Evaluate the model
        mse = mean_squared_error(y_true, predictions)

        return mse

    # Save
    def save(self, model):
        # Save the model
        model.save_model('model.json')

# Define Wheat model
wheat = Crop(
    name="wheat",
    t_base=5.0, 
    stages={
        "sowing": {"day": 111},
        "germination": {"day": 151},
        "tillering": {"day": 182},
        "heading": {"day": 243},
        "maturity": {"day": 304}
    }
)

# Create Supabase client
sb = supabaseInstance().get_client()

# Create model
model = Model(wheat, sb)

# Load data
data = model.load_data()

# Print data
print(data)

# Train model
model.train(data)

# Evaluate model
mse = model.evaluate()

# Print MSE
print(f"Mean Squared Error: {mse}")
