import ee
import os
from google.cloud import storage

# Authenticate and initialize the Earth Engine API
ee.Authenticate()
ee.Initialize(project='mp6-earth-engine')

# Define the dataset and filter by date
dataset = ee.ImageCollection('MODIS/061/MOD11A2') \
           .filter(ee.Filter.date('2012-01-01', '2024-06-01'))

# Select the land surface temperature band
land_surface_temperature = dataset.select('LST_Day_1km')

# Define the region to export (use the entire globe)
region = ee.Geometry.Polygon(
    [[[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]]
)

# Set up Google Cloud Storage client
client = storage.Client()
bucket_name = 'terrabyte_tif'
bucket = client.bucket(bucket_name)

# Function to export each image
def export_image(image):
    date = image.date().format('YYYY-MM-dd').getInfo()
    filename = f'LST_Day_1km_{date}.tif'
    task = ee.batch.Export.image.toCloudStorage(
        image=image,
        description=filename,
        bucket=bucket_name,
        fileNamePrefix=filename,
        scale=1000,
        region=region,
        crs='EPSG:4326',
        maxPixels=1e13
    )
    task.start()
    print(f'Started export for {filename}')
    return filename

# Function to download the exported file from GCS
def download_from_gcs(filename):
    blob = bucket.blob(filename)
    local_path = os.path.join('ge_export', filename)  # Replace with your local directory path
    blob.download_to_filename(local_path)
    print(f'Downloaded {filename} to {local_path}')

# Iterate over each image in the collection and export it
images = land_surface_temperature.toList(land_surface_temperature.size()).getInfo()
for img_info in images:
    img_id = img_info['id']
    img = ee.Image(img_id)
    filename = export_image(img)
    # Wait for the task to complete before downloading
    task = ee.batch.Task.list()[-1]
    task_status = task.status()
    while task_status['state'] in ['READY', 'RUNNING']:
        task_status = task.status()
    if task_status['state'] == 'COMPLETED':
        download_from_gcs(filename)
    else:
        print(f"Task failed for {filename}")

# Optionally, monitor tasks
tasks = ee.batch.Task.list()
for task in tasks:
    print(task)
