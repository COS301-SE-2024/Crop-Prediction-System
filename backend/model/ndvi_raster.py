import rasterio
import matplotlib.pyplot as plt
import numpy as np

from svgpathtools import svg2paths2

filename = 'ndvi_images/sa1214.tif'
svg = 'base_layers/sa_wheat_farmlands.svg'

# Read the NDVI data from the GeoTIFF file
with rasterio.open(filename) as src:
    ndvi_array = src.read(1)  # Assuming NDVI is in the first band
    metadata = src.meta

# Define ROI coordinates (x, y, width, height)
x = 2500
y = 7073
width = 6225
height = 4073

# Crop the ROI from the NDVI array
roi = ndvi_array[y:y+height, x:x+width]

# Remove 0 values (assuming these are nodata or ocean)
roi = np.where(roi == 0.0, np.nan, roi)

# Plot the ROI
# plt.imshow(roi, cmap='viridis')
# plt.colorbar(label='NDVI')
# plt.title('NDVI in ROI')
# plt.show()

# Histogram of NDVI values in the ROI
plt.hist(roi.flatten(), bins=50, color='c')
plt.xlabel('NDVI Values')
plt.ylabel('Frequency')
plt.title('Histogram of NDVI Values in ROI')
plt.show()

# Perform further analysis on the ROI, excluding nan values
roi_no_nan = roi[~np.isnan(roi)]
mean_ndvi = np.mean(roi_no_nan)
median_ndvi = np.median(roi_no_nan)
std_dev_ndvi = np.std(roi_no_nan)
max_ndvi = np.max(roi_no_nan)
min_ndvi = np.min(roi_no_nan)

print("Mean NDVI:", mean_ndvi)
print("Median NDVI:", median_ndvi)
print("Standard Deviation of NDVI:", std_dev_ndvi)
print("Max NDVI:", max_ndvi)
print("Min NDVI:", min_ndvi)

# Normalize NDVI values to range between -1 and 1
normalized_roi = np.apply_along_axis(lambda x: (x - min_ndvi) / (max_ndvi - min_ndvi) * 2 - 1, 0, roi)

# Plot the normalized ROI
plt.imshow(normalized_roi, cmap='viridis')
plt.colorbar(label='Normalized NDVI')
plt.title('Normalized NDVI in ROI')
plt.show()

# For wheat, select the fields with an NDVI between 0.15 and 0.9, and set the rest to NaN
# suitable_wheat_roi = np.where((normalized_roi >= -0.2) & (normalized_roi <= 1), normalized_roi, np.nan)

mask_filename = 'mask.tif'
with rasterio.open(mask_filename) as mask_src:
    mask = mask_src.read(1)

# Apply the mask to the NDVI array
clipped_ndvi_array = np.where(mask, normalized_roi, np.nan)

# Print total number of pixels in the ROI
print("Total number of pixels in the ROI:", np.size(suitable_wheat_roi))

# Print the number of suitable wheat pixels
print("Number of suitable wheat pixels:", np.count_nonzero(~np.isnan(suitable_wheat_roi)))

# Plot a histogram of the suitable wheat ROI
plt.hist(suitable_wheat_roi.flatten(), bins=50, color='c')
plt.xlabel('Normalized NDVI Values')
plt.ylabel('Frequency')
plt.title('Histogram of Normalized NDVI Values Suitable for Wheat')
plt.show()

# Plot the suitable wheat ROI
plt.imshow(suitable_wheat_roi, cmap='viridis')
plt.colorbar(label='Normalized NDVI')
plt.title('Normalized NDVI Suitable for Wheat')
plt.show()

# Perform further analysis on the normalized ROI
suitable_wheat_roi_no_nan = suitable_wheat_roi[~np.isnan(suitable_wheat_roi)]
mean_normalized_ndvi = np.mean(suitable_wheat_roi_no_nan)
median_normalized_ndvi = np.median(suitable_wheat_roi_no_nan)
std_dev_normalized_ndvi = np.std(suitable_wheat_roi_no_nan)
max_normalized_ndvi = np.max(suitable_wheat_roi_no_nan)
min_normalized_ndvi = np.min(suitable_wheat_roi_no_nan)

print("Mean Normalized NDVI:", mean_normalized_ndvi)
print("Median Normalized NDVI:", median_normalized_ndvi)
print("Standard Deviation of Normalized NDVI:", std_dev_normalized_ndvi)
print("Max Normalized NDVI:", max_normalized_ndvi)
print("Min Normalized NDVI:", min_normalized_ndvi)
