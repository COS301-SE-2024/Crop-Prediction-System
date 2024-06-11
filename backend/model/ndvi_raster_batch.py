# Description: This script downloads NDVI data from a URL, extracts the data, and processes it to calculate statistics for a region of interest (ROI).

import requests
import zipfile
import io
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from tqdm import tqdm
import re
from scipy import stats as sp

# Supabase
import supabase
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client = supabase.create_client(supabase_url, supabase_key)

# 72 samples per year. Write a line to add the date to the dataframe (e.g. 2022-01-01). The file name is 2207 which means the 7th sample of 2022. This correlates to about 365/72*7 = 35 days after the start of the year.

# Define function to process each NDVI image
def process_ndvi_image(file_path, x, y, width, height):
    with rasterio.open(file_path) as src:
        ndvi_array = src.read(1)  # Assuming NDVI is in the first band

    # Crop the ROI from the NDVI array
    roi = ndvi_array[y:y+height, x:x+width]

    # Remove 0 values (ocean or nodata) from the ROI
    roi = roi[roi != 0.0]

    # Calculate statistics for the ROI
    # mean_ndvi = roi.mean()
    # median_ndvi = np.median(roi)
    # std_dev_ndvi = roi.std()
    max_ndvi = roi.max()
    min_ndvi = roi.min()

    # Normalize NDVI values to range between -1 and 1
    normalized_roi = (roi - min_ndvi) / (max_ndvi - min_ndvi) * 2 - 1

    # Calculate statistics for the normalized ROI
    mean_normalized_ndvi = normalized_roi.mean()
    median_normalized_ndvi = np.median(normalized_roi)
    mode_normalized_ndvi = sp.mode(normalized_roi)
    variance_normalized_ndvi = np.var(normalized_roi)
    std_dev_normalized_ndvi = normalized_roi.std()
    max_normalized_ndvi = normalized_roi.max()
    min_normalized_ndvi = normalized_roi.min()
    iqr_normalized_ndvi = np.percentile(normalized_roi, 75) - np.percentile(normalized_roi, 25)

    # Count of valid pixels
    valid_pixels = np.count_nonzero(~np.isnan(normalized_roi))

    # Timestamp of the NDVI image
    date_str = os.path.basename(file_path).split('.')[0]
    year = date_str[2:4]
    sample = date_str[4:]
    date = f'20{year}-01-01'
    date = pd.to_datetime(date) + pd.DateOffset(days=int(sample) * 365 / 72)

    # Print confirmation of ndvi image processing
    print("Processed NDVI image: ", file_path, "\n",)

    return {
        'date': date,
        'file_path': file_path,
        'mean_normalized_ndvi': mean_normalized_ndvi,
        'median_normalized_ndvi': median_normalized_ndvi,
        'std_dev_normalized_ndvi': std_dev_normalized_ndvi,
        'max_normalized_ndvi': max_normalized_ndvi,
        'min_normalized_ndvi': min_normalized_ndvi,
        # TODO: Make a decision on which statistics to include in the final DataFrame
        'mode_normalized_ndvi': mode_normalized_ndvi,
        'variance_normalized_ndvi': variance_normalized_ndvi,
        'iqr_normalized_ndvi': iqr_normalized_ndvi,
        'valid_pixels': valid_pixels,
    }

# Define ROI coordinates (x, y, width, height)
x = 2500
y = 7073
width = 6225
height = 4073

# Define URL containing NDVI zip files
ndvi_url = 'https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/fews/web/africa/southern/pentadal/eviirs/ndvi/temporallysmoothedndvi/downloads/pentadal/'

# Fetch URLs of all NDVI zip files from the directory
response = requests.get(ndvi_url)

# Extract links from the HTML content
ndvi_links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)

# Select only the links that contain 'zip' in the URL
ndvi_links = [link for link in ndvi_links if 'zip' in link]

# Prepend the base URL to the relative links
ndvi_links = [ndvi_url + link for link in ndvi_links]

# TODO: Filter the NDVI zip files based on the date range
# Will have to decide on the crop season and filter the NDVI files accordingly

# Take every 6th NDVI zip file (i.e. monthly data)
# ndvi_zip_files = ndvi_links[::6]

ndvi_zip_files = ndvi_links

print("Number of NDVI zip files:", len(ndvi_zip_files))

# Process each NDVI zip file URL
ndvi_data = []
for zip_url in tqdm(ndvi_zip_files, desc="Downloading and Processing", unit="zip file"):
    # Download the zip file
    zip_response = requests.get(zip_url)
    with zipfile.ZipFile(io.BytesIO(zip_response.content)) as zip_ref:
        # Extract all files from the zip
        zip_ref.extractall('temp_folder')
        
        # Process each extracted file
        for file_name in zip_ref.namelist():
            if file_name.endswith('.tif'):
                file_path = os.path.join('temp_folder', file_name)
                
                # Process the NDVI image
                processed_data = process_ndvi_image(file_path, x, y, width, height)

                # Append the processed data to the list
                ndvi_data.append(processed_data)

                # Add to Supabase
                supabase_client.table('historical.ndvi').insert([{
                    'date': processed_data['date'],
                    'file_path': processed_data['file_path'],
                    'mean_normalized_ndvi': processed_data['mean_normalized_ndvi'],
                    'median_normalized_ndvi': processed_data['median_normalized_ndvi'],
                    'std_dev_normalized_ndvi': processed_data['std_dev_normalized_ndvi'],
                    'max_normalized_ndvi': processed_data['max_normalized_ndvi'],
                    'min_normalized_ndvi': processed_data['min_normalized_ndvi'],
                    'mode_normalized_ndvi': processed_data['mode_normalized_ndvi'],
                    'variance_normalized_ndvi': processed_data['variance_normalized_ndvi'],
                    'iqr_normalized_ndvi': processed_data['iqr_normalized_ndvi'],
                    'valid_pixels': processed_data['valid_pixels'],
                }]).execute()

                # Remove tif file after processing
                os.remove(file_path)

# Create a DataFrame from the extracted data
ndvi_df = pd.DataFrame(ndvi_data)

# Print the DataFrame to verify
print(ndvi_df)

# Sort the DataFrame by date
ndvi_df = ndvi_df.sort_values('date')

# Optionally, you can save the DataFrame to a CSV file
ndvi_df.to_csv('ndvi_statistics.csv', index=False)

# Remove the temporary folder after processing
import shutil
shutil.rmtree('temp_folder')
