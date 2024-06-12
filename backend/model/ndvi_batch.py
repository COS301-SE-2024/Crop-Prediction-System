# Description: This script downloads NDVI data from a URL, extracts the data, and processes it to calculate statistics for a region of interest (ROI).

import requests
import zipfile
import io
import os
import pandas as pd
from tqdm import tqdm
import re

from ndvi import process_ndvi_image
import time

# Supabase
# import supabase
# from dotenv import load_dotenv

# load_dotenv()

# # Supabase credentials
# supabase_url = os.environ.get('SUPABASE_URL')
# supabase_key = os.environ.get('SUPABASE_KEY')

# # Initialize Supabase client
# supabase_client = supabase.create_client(supabase_url, supabase_key)

# 72 samples per year. Write a line to add the date to the dataframe (e.g. 2022-01-01). The file name is 2207 which means the 7th sample of 2022. This correlates to about 365/72*7 = 35 days after the start of the year.

def process_ndvi_files():

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
                    
                    timer = time.time()
                    processed_data = process_ndvi_image(file_path)

                    processed_data['date'] = processed_data['date'].isoformat()

                    ndvi_data.append(processed_data)

                    # print(f"Processed {file_path} in {time.time() - timer} seconds")

                    # timer = time.time()

                    # # response = supabase_client.table('ndvi_historical').insert([processed_data]).execute()

                    # print(f"Response: {response} in {time.time() - timer} seconds")

                    # Remove tif file after processing
                    os.remove(file_path)

    # Create a DataFrame from the extracted data
    ndvi_df = pd.DataFrame(ndvi_data)

    # Print the DataFrame to verify
    # print(ndvi_df)

    # # Sort the DataFrame by date
    # ndvi_df = ndvi_df.sort_values('date')

    # # Optionally, you can save the DataFrame to a CSV file
    # ndvi_df.to_csv('ndvi_statistics.csv', index=False)

    # Remove the temporary folder after processing
    import shutil
    shutil.rmtree('temp_folder')

    return ndvi_df
