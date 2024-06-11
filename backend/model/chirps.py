import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Specify the filename of the CHIRPS GeoTIFF file
filename = 'chirps_images/chirps-v2.0.2024.03.tif'

# Open the CHIRPS GeoTIFF file
with rasterio.open(filename) as src:
    chirps_array = src.read(1) # Assuming CHIRPS data is in the first band
    metadata = src.meta

# Define ROI coordinates (x, y, width, height)
x = 3850
y = 1400
width = 500
height = 300

# Crop the ROI from the CHIRPS array
roi = chirps_array[y:y+height, x:x+width]

roi = np.where(roi == -9999, np.nan, roi)

# Print ROI
plt.imshow(roi, cmap='viridis')
plt.colorbar(label='Precipitation (mm/day)')
plt.title('CHIRPS Precipitation Data')
plt.show()

# Plot the ROI with a blue-to-red spectrum colormap
plt.imshow(roi, cmap='bwr', interpolation='nearest')  # 'bwr' colormap for blue-to-red spectrum
plt.colorbar(label='Precipitation (mm/day)')
plt.title('CHIRPS Precipitation Data')
plt.show()

# Remove 0 values (ocean or nodata) from the ROI
roi = roi[roi != 0.0]

# Histogram of CHIRPS values in the ROI
plt.hist(roi.flatten(), bins=50, color='c')
plt.xlabel('Precipitation Values (mm/day)')
plt.ylabel('Frequency')
plt.title('Histogram of Precipitation Values in ROI')
plt.show() 

# Perform further analysis on the ROI
mean_chirps = roi.mean()
median_chirps = np.median(roi)
std_dev_chirps = roi.std()
max_chirps = roi.max()
min_chirps = roi.min()

print("Mean Precipitation:", mean_chirps)
print("Median Precipitation:", median_chirps)
print("Standard Deviation of Precipitation:", std_dev_chirps)
print("Max Precipitation:", max_chirps)
print("Min Precipitation:", min_chirps)
