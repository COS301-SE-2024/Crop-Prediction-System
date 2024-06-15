import csv
import os

# Define file paths
directory = 'uea.ac.uk/csv/'

# Function to read CSV and return a list of dictionaries for each row
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# 2D list to store data from all CSV files
data = []
filenames = []

# Read all csv files in the directory
for filename in os.listdir(directory):
    file_path = directory + filename
    if not file_path.endswith('.csv'):
        continue
    data.append(read_csv(file_path))
    filenames.append(filename)
    print(f'{filename}: {len(data)} rows')

# Remove the .csv extension from the filenames
filenames = [filename[:-4] for filename in filenames]
print(filenames)

# Prepare to combine data
combined_data = []

# Define months
months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

# Iterate through each year and month
for i in range(len(data[0])):
    year = data[0][i]['YEAR']
    for j in range(len(months)):
        month = months[j]
        data_to_append = {
            'date': f'{month}-{year}'
        }
        for k in range(len(data)):
            data_to_append[filenames[k]] = data[k][i][month]
        combined_data.append(data_to_append)

# Write the combined data to a new CSV file
with open('uea_converted.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['date'] + filenames)
    writer.writeheader()
    for row in combined_data:
        writer.writerow(row)

