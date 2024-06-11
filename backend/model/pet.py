import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

file_path = 'pet/et120101.bil'

def process_pet_file(file_path, file_name):

    with rasterio.open(file_path) as src:
        pet_array = src.read(1)
        metadata = src.profile

    # plt.imshow(pet_array, cmap='viridis')
    # plt.colorbar(label='PET (mm/month)')
    # plt.title('Potential Evapotranspiration Data')
    # plt.show()

    # Show in a different style
    # plt.imshow(pet_array, cmap='rainbow')
    # plt.colorbar(label='PET (mm/month)')
    # plt.title('Potential Evapotranspiration Data')
    # plt.show()

    # Define ROI coordinates (x, y, width, height)
    x = 180
    y = 100
    w = 55
    h = 30

    roi = pet_array[y:y+h, x:x+w]

    roi = np.where(roi == -9999, np.nan, roi)

    # Import the mask from a TIFF file
    mask_filename = 'base_layers/sa_wheat_pet.tif'
    with rasterio.open(mask_filename) as mask_src:
        mask = mask_src.read(1)
        mask_metadata = mask_src.meta

    # plt.imshow(mask, cmap='gray')
    # plt.colorbar(label='Mask Value')
    # plt.title('Wheat Farmland Mask')
    # plt.show()

    # Crop the mask to match the dimensions of the ROI
    mask = mask[y:y+h, x:x+w]

    # plt.imshow(mask, cmap='gray')
    # plt.colorbar(label='Mask Value')
    # plt.title('Wheat Farmland Mask')
    # plt.show()

    mask = np.where(mask < 255, 1, 0)

    # Plot the Mask
    # plt.imshow(mask, cmap='gray')
    # plt.colorbar(label='Mask Value')
    # plt.title('Wheat Farmland Mask')
    # plt.show()

    # Resize or interpolate the mask to match the dimensions of the ROI array
    # Use appropriate resizing or interpolation method based on the array dimensions
    # Apply the mask to the ROI array
    roi = np.where(mask == 1, roi, np.nan)

    # Plot the ROI with a blue-to-red spectrum colormap
    # plt.imshow(roi, cmap='rainbow')
    # plt.colorbar(label='PET (mm/month)')
    # plt.title('Potential Evapotranspiration Data')
    # plt.show()

    # apply normalization between -1 and 1
    roi = (roi - np.nanmin(roi)) / (np.nanmax(roi) - np.nanmin(roi))
    roi = 2 * roi - 1

    # Plot the normalized ROI
    # plt.imshow(roi, cmap='rainbow')
    # plt.colorbar(label='Normalized PET')
    # plt.title('Normalized Potential Evapotranspiration Data')
    # plt.show()

    # Calculate statistics
    mean = np.nanmean(roi)
    median = np.nanmedian(roi)
    std = np.nanstd(roi)
    var = np.nanvar(roi)
    iqr = np.nanpercentile(roi, 75) - np.nanpercentile(roi, 25)

    # print(f"Mean: {mean}")
    # print(f"Median: {median}")
    # print(f"Standard Deviation: {std}")
    # print(f"Variance: {var}")
    # print(f"IQR: {iqr}")

    # date
    # print(file_name)
    # et020120.tar.gz

    date = file_name[2:8]
    date = f"{date[:2]}-{date[2:4]}-{date[4:]}"
    date = dt.datetime.strptime(date, "%y-%m-%d")

    return {
        'date': date,
        'mean': mean,
        'median': median,
        'std': std,
        'var': var,
        'iqr': iqr
    }

