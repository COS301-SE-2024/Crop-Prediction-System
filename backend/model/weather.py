import pandas as pd

# Define a chunk size
chunk_size = 1000  # Adjust based on your memory constraints

# Initialize an empty dataframe
df_list = []

# Read the CSV file in chunks
for chunk in pd.read_csv('big_data/weatherdata_v3.csv', chunksize=chunk_size):
    # Process each chunk (optional)
    df_list.append(chunk)

# Concatenate all chunks
df = pd.concat(df_list, axis=0)
