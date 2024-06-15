import os
import re
import numpy as np

def camel_case(s):
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s).title().replace(' ', '')
    return s[0].lower() + s[1:]

def convert_to_csv(file_path, output_dir):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the parameter and units from the file
    parameter_line = lines[1]  # Assuming the parameter line is always the second line
    parameter = parameter_line.split('=')[2].strip().split(':')[0].strip()
    parameter_camel_case = camel_case(parameter)
    
    units_line = lines[1]  # Assuming the units line is part of the second line
    units = units_line.split('=')[3].strip().split(':')[0].strip()
    
    # Split the file content by lines and keep only the data lines
    data_lines = lines[5:]  # Skipping the first 5 lines which are headers
    
    # Remove empty lines
    data_lines = [line for line in data_lines if line.strip()]
    
    # Split each data line into a list of values
    data_array = [line.split() for line in data_lines]
    
    # Convert to numpy array
    data_array = np.array(data_array)
    
    # Remove MAM, JJA, SON, DJF, ANN columns (indices 13 to 17)
    data_array = data_array[:, 0:13]
    
    # Convert each value to float except the first column (year)
    data_array = np.array([[float(value) if i != 0 else value for i, value in enumerate(line)] for line in data_array])
    
    # Add headers for CSV
    headers = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    data_array = np.insert(data_array, 0, headers, axis=0)
    
    # Create output file path
    output_file_path = os.path.join(output_dir, f'{parameter_camel_case}.csv')
    
    # Save to CSV with a description line
    with open(output_file_path, 'w') as output_file:
        output_file.write(f'# Data units: {units}\n')
        np.savetxt(output_file, data_array, fmt='%s', delimiter=',')
    print(f"Converted {file_path} to {output_file_path}")

# Directory containing the .per files
input_directory = 'uea.ac.uk'
output_directory = 'uea.ac.uk/csv'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process each .per file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.per'):
        file_path = os.path.join(input_directory, filename)
        convert_to_csv(file_path, output_directory)
