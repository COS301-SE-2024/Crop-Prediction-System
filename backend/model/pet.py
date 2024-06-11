import requests
import io
import os
import pandas as pd
import numpy as np
import rasterio
from rasterio.io import MemoryFile
from tqdm import tqdm
import re
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import tarfile
import tempfile

from pet_batch import process_pet_file

load_dotenv()

# Supabase credentials
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase_client: Client = create_client(supabase_url, supabase_key)

# Define URL containing PET tar.gz files
pet_url = 'https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/fews/web/global/daily/pet/downloads/daily/'  # Replace with actual URL

# Fetch URLs of all PET tar.gz files from the directory
response = requests.get(pet_url)
response.raise_for_status()

# Extract links from the HTML content
pet_links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
pet_links = [link for link in pet_links if 'tar.gz' in link]
pet_links = [pet_url + link for link in pet_links]

# Select all URLs from et12 to et24
possibilities = ['et12', 'et13', 'et14', 'et15', 'et16', 'et17', 'et18', 'et19', 'et20', 'et21', 'et22', 'et23', 'et24']
pet_links = [link for link in pet_links if any(possibility in link for possibility in possibilities)]

print("Number of PET tar.gz files:", len(pet_links))

# Function to extract .bil and related files from tar.gz archive to a temp directory
def extract_files_to_temp_dir(tar_gz_content, temp_dir):
    with tarfile.open(fileobj=io.BytesIO(tar_gz_content), mode='r:gz') as tar:
        tar.extractall(path=temp_dir)

# Process each PET tar.gz file URL
pet_data = []
for tar_gz_url in tqdm(pet_links, desc="Downloading and Processing PET", unit="tar.gz file"):
    tar_gz_response = requests.get(tar_gz_url)
    with tempfile.TemporaryDirectory() as temp_dir:
        extract_files_to_temp_dir(tar_gz_response.content, temp_dir)
        
        file_name = os.path.basename(tar_gz_url)
        
        # get actual path to the extracted .bil file
        bil_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.bil')]

        print(f"Extracted .bil files: {bil_files}")
        
        processed_data = process_pet_file(bil_files[0], file_name)
        if processed_data is not None:
            processed_data['date'] = processed_data['date'].isoformat()
            pet_data.append(processed_data)
            
            # Uncomment the following lines if you want to insert data into Supabase
            response = supabase_client.table('pet_historical').insert([processed_data]).execute()
            print(f"Response: {response}")

# Create a DataFrame from the extracted data
pet_df = pd.DataFrame(pet_data)

# Sort the DataFrame by date
pet_df = pet_df.sort_values('date')

# Optionally, you can save the DataFrame to a CSV file
pet_df.to_csv('pet_statistics.csv', index=False)
