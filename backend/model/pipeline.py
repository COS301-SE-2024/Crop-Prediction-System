# Defines the base model for crop prediction that predicts yield
from backend.definitions.crop import Crop
from backend.definitions.field import Field
from backend.database.supabaseInstance import supabaseInstance
from backend.database.supabaseFunctions import supabaseFunctions
from backend.model.FusionModel import FusionModel

# Model specific imports
import pandas as pd
import datetime

class Pipeline:
    def __init__(self):
        self.sb = supabaseInstance().get_client()
        self.sf = supabaseFunctions()
        self.model = None

    def train_all(self):
        fields = self.sb.table('field_info').select('id').execute().data
        for field in fields:
            self.train(field['id'])
        return {"status": "All models trained successfully"}

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
        if field_id == None:
            return {
                "error": "Field ID cannot be empty."
            }
        dict = {"fieldid": field_id}
        response = self.sb.rpc('get_data', dict).execute()
        if response.data == []:
            return {"error": "Data not found. Field ID may be invalid or may not have any data."}
        
        model_data = pd.DataFrame(response.data)

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
    def train(self, field_id = None) -> dict:
        # Load the data
        if field_id == None and crop == None:
            return {"error": "Both Field ID and crop name cannot be empty."}
        
        f : Field  = self.sf.getFieldInfo(field_id)
        crop = f.crop_type
        c : Crop = self.sf.getCrop(crop)

        X, y = self.load_data(c, field_id)

        self.model = None # Reset the model
        self.model = FusionModel(X, y, c)
        modelResponse = self.model.train()

        print(modelResponse, flush=True)

        # Replace None with null
        modelResponse = str(modelResponse).replace("None", "0")

        # Extract predictions
        predictions = modelResponse.split("prediction")[1].split("}")[0].replace(":", "").replace("[", "").replace("]", "").replace(" ", "").replace("'", "").split(",")

        # Convert to normal float
        predictions = [float(i) for i in predictions]

        print(predictions, flush=True)

        try:
            for i in range(0,6):
                result = self.sb.table('data').update({
                    'pred_yield': predictions[i]
                }).eq(
                    'field_id', field_id
                ).eq(
                    'date', (datetime.datetime.now() + datetime.timedelta(days=i)).isoformat()
                ).execute()
        except Exception as e:
            pass

        return {
            "status" : "Model trained successfully"
        }

# if __name__ == '__main__':
#     p = Pipeline()
#     p.train("14420bc8-48e3-47bc-ab83-1a6498380588")
    # p.train("975f9c3b-ed7c-49cd-b0e1-99b9c2bd7b9f")