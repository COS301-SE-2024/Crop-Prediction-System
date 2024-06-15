import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# Specify the filename of the CHIRPS GeoTIFF file
filename = 'chirps_images/chirps-v2.0.2024.03.tif'

def process_chirps_image(file_path, file_name):

    # Open the CHIRPS GeoTIFF file from buffer
    with rasterio.open(file_path) as src:
        chirps_array = src.read(1)
        chirps_metadata = src.meta

    # # Define ROI coordinates (x, y, width, height)
    x = 3850
    y = 1400
    width = 500
    height = 300

    # Crop the ROI from the CHIRPS array
    roi = chirps_array[y:y+height, x:x+width]

    roi = np.where(roi == -9999, np.nan, roi)

    # Import the mask from a TIFF file
    mask_filename = 'base_layers/sa_wheat_for_chirps.tif'
    with rasterio.open(mask_filename) as mask_src:
        mask = mask_src.read(1)
        mask_metadata = mask_src.meta

    # plt.imshow(mask, cmap='gray')
    # plt.colorbar(label='Mask Value')
    # plt.title('Wheat Farmland Mask')
    # plt.show()

    # Crop the mask to match the dimensions of the ROI
    mask = mask[y:y+height, x:x+width]

    # plt.imshow(mask, cmap='gray')
    # plt.colorbar(label='Mask Value')
    # plt.title('Wheat Farmland Mask')
    # plt.show()

    mask = np.where(mask == 0, 1, 0)

    # Plot the Mask

    # Resize or interpolate the mask to match the dimensions of the ROI array
    # Use appropriate resizing or interpolation method based on the array dimensions
    # Apply the mask to the ROI array
    roi = np.where(mask == 1, roi, np.nan)

    # Plot the ROI with a blue-to-red spectrum colormap
    # plt.imshow(roi, cmap='bwr', interpolation='nearest')  # 'bwr' colormap for blue-to-red spectrum
    # plt.colorbar(label='Precipitation (mm/day)')
    # plt.title('CHIRPS Precipitation Data')
    # plt.show()

    # # Histogram of CHIRPS values in the ROI
    # plt.hist(roi.flatten(), bins=50, color='c')
    # plt.xlabel('Precipitation Values (mm/day)')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of Precipitation Values in ROI')
    # plt.show()

    # Perform further analysis on the ROI
    roi_non_nan = roi[~np.isnan(roi)]
    mean_chirps = np.mean(roi_non_nan)
    median_chirps = np.median(roi_non_nan)
    std_dev_chirps = np.std(roi_non_nan)
    max_chirps = np.max(roi_non_nan)
    min_chirps = np.min(roi_non_nan)

    variance_chirps = np.var(roi_non_nan)
    iqr_chirps = np.percentile(roi_non_nan, 75) - np.percentile(roi_non_nan, 25)


    # print("Variance of Precipitation:", variance_chirps)

    # print("Mean Precipitation:", mean_chirps)
    # print("Median Precipitation:", median_chirps)
    # print("Standard Deviation of Precipitation:", std_dev_chirps)
    # print("Max Precipitation:", max_chirps)
    # print("Min Precipitation:", min_chirps)

    valid_pixels = np.sum(~np.isnan(roi))

    year = file_name[12:16]
    month = file_name[17:19]
    date = f'{year}-{month}-01'
    date = pd.to_datetime(date)

    print (date)

    # Print confirmation of ndvi image processing
    # print("Processed NDVI image: ", file_path, "\n",)

    return {
        'date': date,
        'file_path': file_name,
        'mean': float(mean_chirps),
        'median': float(median_chirps),
        'stdev': float(std_dev_chirps),
        'var': float(variance_chirps),
        'iqr': float(iqr_chirps),
        'valid_pixels': int(valid_pixels),
    }
