# This script reads all local NDVI images in the 'ndvi_images' directory, extracts a region of interest (ROI) from each image, and calculates statistics for the ROI. The script then normalizes the NDVI values to range between -1 and 1 and calculates statistics for the normalized ROI. The extracted statistics are stored in a pandas DataFrame for further analysis or export to a CSV file.

import os
import pandas as pd

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Supabase credentials
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = create_client(supabase_url, supabase_key)

# timer for performance
import time

from ndvi_clip import process_ndvi_image

# Define ROI coordinates (x, y, width, height)
x = 2500
y = 7073
width = 6225
height = 4073

# Define directory containing NDVI image files
ndvi_dir = 'ndvi_images/'

# List all NDVI image files in the directory
ndvi_files = [os.path.join(ndvi_dir, f) for f in os.listdir(ndvi_dir) if f.endswith('.tif')]

# Process each NDVI image file and store statistics in a list
ndvi_data = []
for file_path in ndvi_files:
    # Process the NDVI image and store the extracted data
    try:
        timer = time.time()
        processed_data = process_ndvi_image(file_path, x, y, width, height)

        processed_data['date'] = processed_data['date'].isoformat()

        ndvi_data.append(processed_data)

        print(f"Processed {file_path} in {time.time() - timer} seconds")

        timer = time.time()

        response = supabase_client.table('ndvi_historical').insert([processed_data]).execute()

        print(f"Response: {response} in {time.time() - timer} seconds")

        # logging.info(f"Supabase response: {response}")
    except Exception as e:
        print(e)

# Create a DataFrame from the extracted data
ndvi_df = pd.DataFrame(ndvi_data)

# Print the DataFrame to verify
print(ndvi_df)

# Sort the DataFrame by date
ndvi_df = ndvi_df.sort_values('date')

# Optionally, you can save the DataFrame to a CSV file
ndvi_df.to_csv('ndvi_local_all.csv', index=False)
