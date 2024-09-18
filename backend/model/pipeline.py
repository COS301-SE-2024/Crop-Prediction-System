# Defines the base model for crop prediction that predicts yield
from pydantic import BaseModel
from backend.definitions.crop import Crop
from backend.database.supabaseInstance import supabaseInstance
from backend.database.supabaseFunctions import supabaseFunctions
from backend.model.FusionModel import FusionModel

# Model specific imports
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import datetime
import os

class Pipeline:
    def __init__(self):
        self.sb = supabaseInstance().get_client()
        self.sf = supabaseFunctions()
        self.model = None

    # Load data
    def load_data(self, crop : Crop, field_id = None) -> pd.DataFrame:
        # print(f"Loading data for field ID: {field_id} and crop: {crop}", flush=True)
        try:
            training_data = self.load_model_data(field_id)
            if "error" in training_data:
                return training_data  # Return the error message if data loading failed

            # Load historical data
            target_data = self.load_yields(crop)
            if "error" in target_data:
                return target_data  # Return the error message if data loading failed
            
            # Convert to DataFrame
            training_data = pd.DataFrame(training_data)
            target_data = pd.DataFrame(target_data)

            # Drop columns that are null
            training_data.dropna(axis=1, inplace=True)
            target_data.dropna(axis=1, inplace=True)

            return training_data, target_data
            
        except Exception as e:
            return {"error": f"An error occurred while loading data: {str(e)}"}
        
    def load_model_data(self, field_id = None) -> pd.DataFrame:
        dict = {"fieldid": field_id} if field_id else {}
        response = self.sb.rpc('get_data', dict).execute()
        if response.data == []:
            return {"error": "Data not found. Field ID may be invalid or may not have any data."}
        
        model_data = pd.DataFrame(response.data)

        # Drop yield column if it exists
        if 'pred_yield' in model_data.columns:
            model_data.drop('pred_yield', axis=1, inplace=True)

        return model_data
        
    def load_yields(self, c : Crop) -> pd.DataFrame:
        cropClass = c.name + "_ton_per_hectare"
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
        historical_data['year'] = historical_data['production_year'].str[0:4].astype(int)
        
        # Drop 'production_year' column
        historical_data.drop('production_year', axis=1, inplace=True)
        
        # Return the cleaned DataFrame
        return historical_data

    # Train
    def train(self, field_id = None, crop = None):
        # Load the data
        if field_id == None and crop == None:
            return {"error": "Both Field ID and crop name cannot be empty."}
        
        c : Crop = None
        if crop == None:
            f = self.sf.getFieldInfo(field_id)
            crop = f.crop_type
            c = self.sf.getCrop(crop)
        else:
            c = self.sf.getCrop(crop)

        X, y = self.load_data(c, field_id)

        self.model = FusionModel(X, y, c)
        print(self.model.train())

        return {
            "status" : "Model trained successfully",
            # "mse" : mse,
            # "rmse" : rmse,
            # "predictions" : prediction
        }

    # Predict
    def predict(self, field_id, test=False):
        return {"error": "Not implemented"}

if __name__ == '__main__':
    p = Pipeline()
    p.train(None, "wheat")