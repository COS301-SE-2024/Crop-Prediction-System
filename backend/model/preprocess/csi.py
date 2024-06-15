# generates a 12-month time series of wheat growth conditions based on the processed NDVI, CHIRPS, and PET data.

# Create a normalized crop stage index (CSI) ranging from 0 to 1, where:

    # 0 represents the start of the planting season.
    # 1 represents the point of harvest.

# In South Africa, planting typically occurs in March, and harvest occurs in August-February, depending on the region.
# The CSI is calculated setting up 12 months of data, with each month representing a stage of crop development.

# The CSI is calculated as follows:
# taken every 5 days
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_csi(total_years, gdd):
    csi_df = []

    for year in range(total_years):
        # Parameters
        measurement_interval = 5

        # Select a random harvest month between August (month 8) and February (month 2)

        # Calculate total days between planting and harvest
        total_days = gdd.iloc[year]['gdd']
        total_days = int(total_days)
        measurement_days = total_days // measurement_interval

        # print("Total days: ", total_days)
        # print("Measurement days: ", measurement_days)

        # Create a logistic growth function with emphasis on early growth
        def logistic_growth(x, L=1, k=1, x0=measurement_days / 4):
            return L / (1 + np.exp(-k * (x - x0)))

        # Generate CSI values
        csi = [1]

        # Generate logistic growth for the days between planting and harvest
        x_values = np.linspace(0, measurement_days, measurement_days)
        csi_values = logistic_growth(x_values, L=1, k=0.3, x0=measurement_days / 4)

        csi.extend(csi_values)

        # Nullify the days after harvest
        for i in range((365 - total_days)):
            csi.append(0.9998)

        csi = [1 - value for value in csi]

        # Plot the CSI & circle the harvest month
        # plt.plot(csi)
        # plt.scatter(harvest_month * days_per_month // measurement_interval, csi[harvest_month * days_per_month // measurement_interval], color='red')
        # plt.xlabel('Resoluted Time (5 days)')
        # plt.ylabel('Crop Stage Index (CSI)')
        # plt.title('Crop Stage Index (CSI) Over the Year')
        # plt.show()

        # print(csi)

        # 1950-07 to 1950
        yearToAppend = gdd.iloc[year]['year']
        yearToAppend = yearToAppend.split('-')[0]

        # Add relative days to the CSI
        planting_date = f"{yearToAppend}-03-01"

        # Take every 5th entry after the planting date
        dateToAppend = pd.date_range(start=planting_date, freq='5D', periods=(365//5))

        # trim csi to the length of dateToAppend
        csi = csi[:len(dateToAppend)]

        csi_df.append(pd.DataFrame({
            'date': dateToAppend,
            'csi': csi
        }))

    # Plot the CSI & circle the harvest month
    # plt.plot(csi)
    # plt.scatter(harvest_month * days_per_month // measurement_interval, csi[harvest_month * days_per_month // measurement_interval], color='red')
    # plt.xlabel('Resoluted Time (5 days)')
    # plt.ylabel('Crop Stage Index (CSI)')
    # plt.title('Crop Stage Index (CSI) Over the Year')
    # plt.show()

    # print(csi)

    return csi_df

# Calculate the CSI from 1920 to 2024

# Import gdd from growing_season.csv
gdd = pd.read_csv('growing_season.csv')
total_years = gdd.shape[0]

print(total_years)
expected_entries = total_years * 72


# Iterate through each year and calculate the CSI
df = calculate_csi(total_years, gdd)

# Write the CSI values to a CSV file
df = pd.concat(df)

df.to_csv('csi.csv', index=False)

# Crop Development Index (CDI) is the product of the normalized NDVI, PET, and CHIRPS values.
# CDI = (NDVI - NDVI_min) / (NDVI_max - NDVI_min) * (PET - PET_min) / (PET_max - PET_min) * (1 - CHIRPS / CHIRPS_max)