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
    std_dev_normalized_ndvi = normalized_roi.std()
    max_normalized_ndvi = normalized_roi.max()
    min_normalized_ndvi = normalized_roi.min()

    return {
        'file_path': file_path,
        # 'mean_ndvi': mean_ndvi,
        # 'median_ndvi': median_ndvi,
        # 'std_dev_ndvi': std_dev_ndvi,
        # 'max_ndvi': max_ndvi,
        # 'min_ndvi': min_ndvi,
        'mean_normalized_ndvi': mean_normalized_ndvi,
        'median_normalized_ndvi': median_normalized_ndvi,
        'std_dev_normalized_ndvi': std_dev_normalized_ndvi,
        'max_normalized_ndvi': max_normalized_ndvi,
        'min_normalized_ndvi': min_normalized_ndvi
        # TODO: Make a decision on which statistics to include in the final DataFrame
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
                ndvi_data.append(process_ndvi_image(file_path, x, y, width, height))

# Create a DataFrame from the extracted data
ndvi_df = pd.DataFrame(ndvi_data)

# Print the DataFrame to verify
print(ndvi_df)

# Optionally, you can save the DataFrame to a CSV file
ndvi_df.to_csv('ndvi_statistics.csv', index=False)

# Remove the temporary folder after processing
import shutil
shutil.rmtree('temp_folder')
