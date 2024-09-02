# Defines the base model for crop prediction that predicts yield
from pydantic import BaseModel
from backend.definitions.crop import Crop
from backend.database.supabaseInstance import supabaseInstance
from backend.database.supabaseFunctions import supabaseFunctions

# Model specific imports
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
import datetime
import os

class Model:
    def __init__(self):
        self.sb = supabaseInstance().get_client()
        self.sf = supabaseFunctions()

    def train_all(self):
        fields = self.sb.table('field_info').select('id').execute().data
        for field in fields:
            self.train(field['id'])
        return {"status": "All models trained successfully"}
        
    def predict_all(self):
        fields = self.sb.table('field_info').select('id').execute().data
        for field in fields:
            self.predict(field['id'])
        return {"status": "All fields predicted successfully"}

    # Load data
    def load_data(self, field_id = None, crop : Crop = None) -> pd.DataFrame:
        if field_id == None and crop.name == None:
            return {"error": "Both Field ID and crop name cannot be empty."}
        try:
            model_data = self.load_model_data(field_id)
            if "error" in model_data:
                return model_data  # Return the error message if data loading failed
            
            c = None
            if crop.name == None:
                print("Crop name not provided. Using field ID to determine crop.", flush=True)
                f = self.sf.getFieldInfo(field_id)
                print(f, flush=True)
                crop = f.crop_type
                c = self.sf.getCrop(crop)
            else:
                c = self.sf.getCrop(crop)

            # Load historical data
            historical_data = self.load_yields(c)
            if "error" in historical_data:
                return historical_data  # Return the error message if data loading failed

            # Merge data and historical_data on the 'year' column
            data = pd.merge(model_data, historical_data, on='year', how='left')

            return data
        except Exception as e:
            return {"error": f"An error occurred while loading data: {str(e)}"}
        
    def load_model_data(self, field_id = None) -> pd.DataFrame:
        dict = {"fieldid": field_id} if field_id else {}
        response = self.sb.rpc('get_model_data', dict).execute()
        if response.data == []:
            return {"error": "Data not found. Field ID may be invalid or may not have any data."}
        
        model_data = pd.DataFrame(response.data)

        # Drop yield column if it exists
        if 'yield' in model_data.columns:
            model_data.drop('yield', axis=1, inplace=True)

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
        historical_data['year'] = historical_data['production_year'].str[0:4].astype(int) + 1
        
        # Drop 'production_year' column
        historical_data.drop('production_year', axis=1, inplace=True)
        
        # Return the cleaned DataFrame
        return historical_data

    # Train
    def train(self, field_id = None, crop = None):
        # Load the data
        if field_id == None and crop == None:
            return {"error": "Both Field ID and crop name cannot be empty."}
        
        data = self.load_data(field_id, crop)

        c : Crop = None
        if crop == None:
            f = self.sf.getFieldInfo(field_id)
            crop = f.crop_type
            c = self.sf.getCrop(crop)
        else:
            c = self.sf.getCrop(crop)

        # print(f"Data loaded for crop: {crop}", flush=True)

        # Get the current stage
        current_stage = self.sf.getCurrentStage(c)

        # print(f"Current stage: {current_stage}", flush=True)

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
        # First delete the existing model
        try:
            os.remove(f"{field_id}.json")
        except:
            pass
        
        best_model.save_model(f"{field_id}.json")
        # self.save(field_id)

        prediction = self.predict(field_id)

        print(f"Mean Squared Error: {mse}", flush=True)
        print(f"Predictions: {prediction}", flush=True)
        return {
            "status" : "Model trained successfully",
            "mse" : mse,
            "predictions" : prediction
        }

    # Predict
    def predict(self, field_id, test=False):
        # Load the model
        # model_response = self.sb.table('model').select('model').eq('field_id', field_id).execute()
        # if model_response.data == []:
        #     return {"error": "Model not found. Field ID may be invalid or may not have a model."}

        dict = {"fieldid": field_id} if field_id else {}
        response = self.sb.rpc('get_model_data', dict).execute()

        data = pd.DataFrame(response.data)

        print(data, flush=True)

        # Exclude rows where 'field_id' is null
        data = data[data['field_id'].notnull()]

        # Load the model
        model = xgb.Booster()
        # model.load_model(model_response.data[0]['model'])
        try:
            model.load_model(f"{field_id}.json")
        except:
            return self.train(field_id)

        # drop  Invalid columns:id: object, field_id: object, stage: object, yield: objec
        data = data.drop(['id', 'field_id', 'stage', 'yield', 'year'], axis=1)

        # Convert data to a DMatrix
        dmatrix = xgb.DMatrix(data)

        # Make predictions
        predictions = model.predict(dmatrix)
        if not test:
            # Upsert the predictions
            try:
                result = self.sb.table('field_data').upsert({
                    'field_id': field_id,
                    'date': datetime.datetime.now().isoformat(),
                    'yield': predictions.tolist()[0]
                }).execute()

                print(f"Predictions upserted successfully: {result}", flush=True)
            except Exception as e:
                print(f"An error occurred while upserting predictions: {str(e)}", flush=True)

        return predictions.tolist()[0] if predictions else None

    # # Evaluate
    # def evaluate(self):
    #     # Load the model
    #     model = xgb.Booster()
    #     model.load_model('model.json')

    #     # Load the data
    #     data = self.load_data()

    #     today = datetime.datetime.now() 
    #     day_of_year = today.timetuple().tm_yday

    #     xgbins = [stage['day'] for stage in self.crop.stages.values()]
    #     # append the last day of the year
    #     xgbins.append(365)

    #     # Determine the current stage
    #     current_stage = pd.cut([day_of_year], bins=xgbins, labels=self.crop.stages.keys())[0]

    #     print(f"Current stage: {current_stage}")

    #     # Filter data based on the current stage
    #     stage_data = data[data['stage'] == current_stage]

    #     X = stage_data.drop(['year', 'stage', 'yield', 'field_id', 'id'], axis=1)
    #     y_true = stage_data['yield']  # Assuming 'yield' is the actual target value you want to compare against

    #     # Convert X to a DMatrix
    #     dmatrix = xgb.DMatrix(X)

    #     # Make predictions
    #     predictions = model.predict(dmatrix)

    #     # Evaluate the model
    #     mse = mean_squared_error(y_true, predictions)

    #     return mse

# Define Wheat model
# wheat = Crop(
#     name="wheat",
#     t_base=5.0, 
#     stages={
#         "sowing": {"day": 111},
#         "germination": {"day": 151},
#         "tillering": {"day": 182},
#         "heading": {"day": 243},
#         "maturity": {"day": 304}
#     }
# )

# # Create Supabase client
# sb = supabaseInstance().get_client()

# # Create model
# model = Model(wheat, sb)

# # Load data
# data = model.load_data()

# # Print data
# print(data)

# # Train model
# model.train(data)

# # Evaluate model
# mse = model.evaluate()

# # Print MSE
# print(f"Mean Squared Error: {mse}")
