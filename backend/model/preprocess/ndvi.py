import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy as sp

def process_ndvi_image(file_path):

    # Read the NDVI data from the GeoTIFF file
    with rasterio.open(file_path) as src:
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

    # Normalize NDVI values to range between -1 and 1
    min_ndvi = np.nanmin(roi)
    max_ndvi = np.nanmax(roi)
    normalized_roi = 2 * ((roi - min_ndvi) / (max_ndvi - min_ndvi)) - 1

    # Load the mask from a TIFF file
    mask_filename = 'base_layers/sa_wheat_farmlands.tif'
    with rasterio.open(mask_filename) as mask_src:
        mask = mask_src.read(1)
        mask_metadata = mask_src.meta

    # Crop the mask to match the dimensions of the ROI
    mask = mask[y:y+height, x:x+width]

    mask = np.where(mask == 0, 1, 0)

    # Plot the mask
    # plt.imshow(mask, cmap='gray')
    # plt.colorbar(label='Mask Value')
    # plt.title('Wheat Farmland Mask')
    # plt.show()

    # Resize or interpolate the mask to match the dimensions of the normalized ROI array
    # Use appropriate resizing or interpolation method based on the array dimensions
    # Apply the mask to the normalized ROI array
    suitable_wheat_roi = np.where(mask == 1, normalized_roi, np.nan)

    # Plot a histogram of the suitable wheat ROI
    # plt.hist(suitable_wheat_roi[~np.isnan(suitable_wheat_roi)].flatten(), bins=50, color='c')
    # plt.xlabel('Normalized NDVI Values')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of Normalized NDVI Values Suitable for Wheat')
    # plt.show()

    # Plot the suitable wheat ROI
    # plt.imshow(suitable_wheat_roi, cmap='viridis')
    # plt.colorbar(label='Normalized NDVI')
    # plt.title('Normalized NDVI Suitable for Wheat')
    # plt.show()

    # Perform further analysis on the normalized ROI
    mean_normalized_ndvi = np.nanmean(suitable_wheat_roi)
    median_normalized_ndvi = np.nanmedian(suitable_wheat_roi)
    std_dev_normalized_ndvi = np.nanstd(suitable_wheat_roi)
    # max_normalized_ndvi = np.nanmax(suitable_wheat_roi)
    # min_normalized_ndvi = np.nanmin(suitable_wheat_roi)

    # Additional statistics for the normalized ROI
    # mode_normalized_ndvi = sp.stats.mode(suitable_wheat_roi)
    variance_normalized_ndvi = np.nanvar(suitable_wheat_roi)
    iqr_normalized_ndvi = np.nanpercentile(suitable_wheat_roi, 75) - np.nanpercentile(suitable_wheat_roi, 25)

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
        'mean': mean_normalized_ndvi,
        'median': median_normalized_ndvi,
        'stdev': std_dev_normalized_ndvi,
        # 'mode': mode_normalized_ndvi[0],
        # 'mode_count': mode_normalized_ndvi[1][0],
        'var': variance_normalized_ndvi,
        'iqr': iqr_normalized_ndvi,
        'valid_pixels': valid_pixels,
    }

