# This script reads all local NDVI images in the 'ndvi_images' directory, extracts a region of interest (ROI) from each image, and calculates statistics for the ROI. The script then normalizes the NDVI values to range between -1 and 1 and calculates statistics for the normalized ROI. The extracted statistics are stored in a pandas DataFrame for further analysis or export to a CSV file.

import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

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
    ndvi_data.append(process_ndvi_image(file_path, x, y, width, height))

# Create a DataFrame from the extracted data
ndvi_df = pd.DataFrame(ndvi_data)

# Print the DataFrame to verify
print(ndvi_df)

# Optionally, you can save the DataFrame to a CSV file
ndvi_df.to_csv('ndvi_local_all.csv', index=False)
