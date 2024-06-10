# This script reads a raster file (e.g., GeoTIFF) containing NDVI values, extracts a region of interest (ROI) from the raster, and performs basic analysis on the ROI, such as calculating mean, median, standard deviation, max, and min NDVI values. It also normalizes the NDVI values to a specified range (e.g., 0-1 or -1 to 1) and performs analysis on the normalized NDVI values.

import rasterio
import matplotlib.pyplot as plt
import numpy as np

filename = 'ndvi_images/sa1207.tif'

with rasterio.open(filename) as src:
    ndvi_array = src.read(1) # Assuming NDVI is in the first band
    metadata = src.meta

# NDVI values in the ndvi_array variable

# Define ROI coordinates (x, y, width, height)
x = 2500
y = 7073
width = 6225
height = 4073

# Crop the ROI from the NDVI array
roi = ndvi_array[y:y+height, x:x+width]

# Plot the ROI
plt.imshow(roi, cmap='viridis')
plt.show()

# Perform further analysis on the ROI
mean_ndvi = roi.mean()
median_ndvi = np.median(roi)
std_dev_ndvi = roi.std()
max_ndvi = roi.max()
min_ndvi = roi.min()

print("Mean NDVI:", mean_ndvi)
print("Median NDVI:", median_ndvi)
print("Standard Deviation of NDVI:", std_dev_ndvi)
print("Max NDVI:", max_ndvi)
print("Min NDVI:", min_ndvi)

# Normalize NDVI values to range between 0 and 1
# normalized_roi = (roi - min_ndvi) / (max_ndvi - min_ndvi)

# Normalize NDVI values to range between -1 and 1
normalized_roi = (roi - min_ndvi) / (max_ndvi - min_ndvi) * 2 - 1

# Plot the normalized ROI (to verify the normalization)
plt.imshow(normalized_roi, cmap='viridis')
plt.show()

# Perform further analysis on the normalized ROI
mean_normalized_ndvi = normalized_roi.mean()
median_normalized_ndvi = np.median(normalized_roi)
std_dev_normalized_ndvi = normalized_roi.std()
max_normalized_ndvi = normalized_roi.max()
min_normalized_ndvi = normalized_roi.min()

print("Mean Normalized NDVI:", mean_normalized_ndvi)
print("Median Normalized NDVI:", median_normalized_ndvi)
print("Standard Deviation of Normalized NDVI:", std_dev_normalized_ndvi)
print("Max Normalized NDVI:", max_normalized_ndvi)
print("Min Normalized NDVI:", min_normalized_ndvi)