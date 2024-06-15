# Preprocesses the data and uploads it to the Supabase database.
from pet_batch import process_pet_files
from ndvi_batch import process_ndvi_files
from chirps_batch import process_chirps_files

from csi import calculate_csi

from dotenv import load_dotenv
import os

from supabase import create_client

load_dotenv()

# Supabase credentials
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = create_client(supabase_url, supabase_key)

# Process PET files
# Returns a pd.DataFrame with processed PET data
# PET data is pentadal
# pet_data = process_pet_files()
# pet_data.to_csv('pet_data.csv', index=False)

# Process CHIRPS files
# Returns a pd.DataFrame with processed CHIRPS data
# CHIRPS data is monthly
# chirps_data = process_chirps_files()
# chirps_data.to_csv('chirps_data_v2.csv', index=False)

# Process NDVI files
# Returns a pd.DataFrame with processed NDVI data
# NDVI data is pentadal
ndvi_data = process_ndvi_files()
ndvi_data.to_csv('ndvi_data.csv', index=False)

# Prepare the data for upload to Supabase
# Select the mean, standard deviation, and date of the PET, NDVI, and CHIRPS data
# For each year, calculate the Crop State Index (CSI) based on the processed NDVI, CHIRPS, and PET data
# pet_data = pet_data.groupby('date').agg({'pet': ['mean', 'std']}).reset_index()
# ndvi_data = ndvi_data.groupby('date').agg({'ndvi': ['mean', 'std']}).reset_index()
# chirps_data = chirps_data.groupby('date').agg({'precipitation': ['mean', 'std']}).reset_index()

# # Merge the dataframes
# data = pet_data.merge(ndvi_data, on='date').merge(chirps_data, on='date')

# # save as csv
# data.to_csv('data.csv', index=False)

# # data entries contain 72 entries per year, calculate the CSI for each year
# csi = []
# for year in data['date'].dt.year.unique():
#     csi.extend(calculate_csi(year))

# # iterate through the data and add the CSI
# data['csi'] = csi

# # Save the data to a CSV file
# data.to_csv('processed_data.csv', index=False)

# print(data)

# # Upload the processed data to the Supabase database
# # Table is in the format of:
# # date | pet_mean | pet_std | ndvi_mean | ndvi_std | precipitation_mean | precipitation_std | csi
# response = supabase_client.table('processed_data').insert(data.to_dict(orient='records')).execute()
