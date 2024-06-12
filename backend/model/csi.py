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

def calculate_csi():

    # Parameters
    planting_month = 0
    days_per_month = 30
    measurement_interval = 5

    # Select a random harvest month between August (month 8) and February (month 2)
    harvest_month = random.choice([5, 6, 7, 8, 9, 10, 11])

    # Calculate total days between planting and harvest
    total_days = (harvest_month - planting_month) * days_per_month
    measurement_days = total_days // measurement_interval

    # Create a logistic growth function with emphasis on early growth
    def logistic_growth(x, L=1, k=1, x0=measurement_days / 4):
        return L / (1 + np.exp(-k * (x - x0)))

    # Generate CSI values
    csi = []

    # Generate logistic growth for the days between planting and harvest
    x_values = np.linspace(0, measurement_days, measurement_days)
    csi_values = logistic_growth(x_values, L=1, k=0.3, x0=measurement_days / 4)

    csi.extend(csi_values)

    # Nullify the days after harvest
    for i in range((12 - harvest_month) * days_per_month // measurement_interval):
        csi.append(1)

    csi = [1 - value for value in csi]

    # Plot the CSI & circle the harvest month
    plt.plot(csi)
    plt.scatter(harvest_month * days_per_month // measurement_interval, csi[harvest_month * days_per_month // measurement_interval], color='red')
    plt.xlabel('Resoluted Time (5 days)')
    plt.ylabel('Crop Stage Index (CSI)')
    plt.title('Crop Stage Index (CSI) Over the Year')
    plt.show()

    print(csi)

    return csi

# Crop Development Index (CDI) is the product of the normalized NDVI, PET, and CHIRPS values.
# CDI = (NDVI - NDVI_min) / (NDVI_max - NDVI_min) * (PET - PET_min) / (PET_max - PET_min) * (1 - CHIRPS / CHIRPS_max)