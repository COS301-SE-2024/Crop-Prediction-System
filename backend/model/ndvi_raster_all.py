# This script reads all local NDVI images in the 'ndvi_images' directory, extracts a region of interest (ROI) from each image, and calculates statistics for the ROI. The script then normalizes the NDVI values to range between -1 and 1 and calculates statistics for the normalized ROI. The extracted statistics are stored in a pandas DataFrame for further analysis or export to a CSV file.

import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy as sp

# # Supabase
# from dotenv import load_dotenv
# from supabase import create_client, Client

# import logging

# # Load environment variables
# load_dotenv()

# # Get Supabase URL and Key
# supabase_url = os.environ.get("SUPABASE_URL")
# supabase_key = os.environ.get("SUPABASE_KEY")

# # Create Supabase client
# supabase_client = create_client(supabase_url, supabase_key)

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

    # Additional statistics for the normalized ROI
    variance_normalized_ndvi = np.var(normalized_roi)
    iqr_normalized_ndvi = np.percentile(normalized_roi, 75) - np.percentile(normalized_roi, 25)
    mode_normalized_ndvi = sp.stats.mode(normalized_roi)

    valid_pixels = np.count_nonzero(~np.isnan(normalized_roi))

    # Timestamp of the NDVI image
    # filename: sa2207.tif
    date_str = os.path.basename(file_path).split('.')[0]
    year = date_str[2:4]
    sample = date_str[4:]
    date = f'20{year}-01-01'
    date = pd.to_datetime(date) + pd.DateOffset(days=int(sample) * 365 / 72)

    print(date)


    return {
        'file_path': file_path,
        'date': date,
        'mean_normalized_ndvi': float(mean_normalized_ndvi),
        'median_normalized_ndvi': float(median_normalized_ndvi),
        'std_dev_normalized_ndvi': float(std_dev_normalized_ndvi),
        'max_normalized_ndvi': float(max_normalized_ndvi),
        'min_normalized_ndvi': float(min_normalized_ndvi),
        'variance_normalized_ndvi': float(variance_normalized_ndvi),
        'iqr_normalized_ndvi': float(iqr_normalized_ndvi),
        'mode_normalized_ndvi': float(mode_normalized_ndvi[0]),
        'mode_normalized_ndvi_count': float(mode_normalized_ndvi[1]),
        'valid_pixels': int(valid_pixels),
    }

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
        processed_data = process_ndvi_image(file_path, x, y, width, height)

        processed_data['date'] = processed_data['date'].isoformat()

        ndvi_data.append(processed_data)

        # response = supabase_client.schema('public').table('ndvi').insert([{
        #     "date": processed_data['date'],
        #     "file_path": processed_data['file_path'],
        #     "mean": processed_data['mean_normalized_ndvi'],
        #     "median": processed_data['median_normalized_ndvi'],
        #     "stdev": processed_data['std_dev_normalized_ndvi'],
        #     "var": processed_data['variance_normalized_ndvi'],
        #     "iqr": processed_data['iqr_normalized_ndvi'],
        #     "mode": processed_data['mode_normalized_ndvi'],
        #     "mode_count": processed_data['mode_normalized_ndvi_count'],
        #     "valid_pixels": processed_data['valid_pixels'],
        # }]).execute()

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
