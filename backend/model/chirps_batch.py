import requests
import gzip
import io
import os
import pandas as pd
from tqdm import tqdm
import re

from chirps import process_chirps_image
import time

# # Supabase
# import supabase
# from dotenv import load_dotenv

# load_dotenv()

# # Supabase credentials
# supabase_url = os.environ.get('SUPABASE_URL')
# supabase_key = os.environ.get('SUPABASE_KEY')

# # Initialize Supabase client
# supabase_client = supabase.create_client(supabase_url, supabase_key)

def process_chirps_files():

    # Define URL containing chirps gz files
    chirps_url = 'https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/fews/web/global/monthly/chirps/final/downloads/monthly/'

    # Fetch URLs of all chirps gz files from the directory
    response = requests.get(chirps_url)

    # Extract links from the HTML content
    chirps_links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)

    # Select only the links that contain 'gz' in the URL
    chirps_links = [link for link in chirps_links if 'gz' in link]

    # Prepend the base URL to the relative links
    chirps_links = [chirps_url + link for link in chirps_links]

    # Select all URLs from 2012-current
    chirps_links = [link for link in chirps_links if '2012' in link or '2013' in link or '2014' in link or '2015' in link or '2016' in link or '2017' in link or '2018' in link or '2019' in link or '2020' in link or '2021' in link or '2022' in link]

    print("Number of chirps gz files:", len(chirps_links))

    # Process each chirps gz file URL
    chirps_data = []
    for gz_url in tqdm(chirps_links, desc="Downloading and Processing", unit="gz file"):
        # Download the gz file
        gz_response = requests.get(gz_url)
        with gzip.GzipFile(fileobj=io.BytesIO(gz_response.content)) as gz_file:
            # Extract data from gz file
            # Assuming there's only one file in each gz archive
            file_content = gz_file.read()
            file_name = os.path.basename(gz_url)
            # Process the extracted data
            with io.BytesIO(file_content) as file_buffer:
                processed_data = process_chirps_image(file_buffer, file_name)
                processed_data['date'] = processed_data['date'].isoformat()
                chirps_data.append(processed_data)
                
                # timer = time.time()
                # response = supabase_client.table('chirps_historical').insert([processed_data]).execute()
                # print(f"Response: {response} in {time.time() - timer} seconds")

    # Create a DataFrame from the extracted data
    chirps_df = pd.DataFrame(chirps_data)

    # # Sort the DataFrame by date
    # chirps_df = chirps_df.sort_values('date')

    # # Optionally, you can save the DataFrame to a CSV file
    # chirps_df.to_csv('chirps_statistics.csv', index=False)

    return chirps_df
