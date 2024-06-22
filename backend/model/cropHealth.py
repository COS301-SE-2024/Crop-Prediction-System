import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def calculateHealth(dFrame, crop, n, optimums=None):
    dFrame = pd.read_csv('backend/model/processed_data/model_data_soil_moisture.csv')
    dFrame = pd.DataFrame(dFrame)

    # Ensure crop is in title case
    crop = crop.title()
    if optimums is None:
        optimums = pd.read_csv('backend/model/optimums.csv')
        optimums = pd.DataFrame(optimums)

    tmin = optimums.loc[optimums['Crop'] == crop, 'Tmin']
    tmax = optimums.loc[optimums['Crop'] == crop, 'Tmax']
    pmin = optimums.loc[optimums['Crop'] == crop, 'Pmin']
    pmax = optimums.loc[optimums['Crop'] == crop, 'Pmax']
    smmin = optimums.loc[optimums['Crop'] == crop, 'SMmin']
    smmax = optimums.loc[optimums['Crop'] == crop, 'SMmax']

    # print(tmin, tmax, pmin, pmax, smmin, smmax)
    
    tmean = float((tmin + tmax) / 2)
    pmean = float((pmin + pmax) / 2)
    smmean = float((smmin + smmax) / 2)

    # print(tmean, pmean, smmean)

    dFrame['temperature_score'] = dFrame['mean_temperature'] / tmean
    dFrame['precipitation_score'] = dFrame['precipitation'] / pmean
    dFrame['soil_moisture_score'] = dFrame['soil_moisture'] / smmean
    dFrame['nutrient_availability_score'] = (dFrame['soil_mineral_fertilizers_nitrogen'] + dFrame['soil_manure_applied_to_soils_nitrogen'] + dFrame['soil_atmospheric_deposition_nitrogen'] + dFrame['soil_biological_fixation_nitrogen']) / 4

    # print(dFrame['temperature_score'])
    # print(dFrame['precipitation_score'])
    # print(dFrame['soil_moisture_score'])
    # print(dFrame['nutrient_availability_score'])

    # Normalize the scores
    dFrame['temperature_score'] = dFrame['temperature_score'] / dFrame['temperature_score'].max()
    dFrame['precipitation_score'] = dFrame['precipitation_score'] / dFrame['precipitation_score'].max()
    dFrame['soil_moisture_score'] = dFrame['soil_moisture_score'] / dFrame['soil_moisture_score'].max()
    dFrame['nutrient_availability_score'] = dFrame['nutrient_availability_score'] / dFrame['nutrient_availability_score'].max()

    # Calculate the health score
    dFrame['health_score'] = (dFrame['temperature_score'] + dFrame['precipitation_score'] + dFrame['soil_moisture_score'] + dFrame['nutrient_availability_score']) / 4


    # Normalize the health score
    dFrame['health_score'] = dFrame['health_score'] / dFrame['health_score'].max()

    # print(dFrame['health_score'])

    # Drop unnecessary columns
    dFrame.drop(columns=['temperature_score', 'precipitation_score', 'soil_moisture_score', 'nutrient_availability_score'], inplace=True)

    # Convert to array
    arr = dFrame['health_score'].tail(n).values

    # Convert to list
    arr = arr.tolist()

    result = {
        'crop': crop,
        'health_score': arr
    }

    return result

# # Sample usage
# res = calculateHealth(None, 'Maize', 10)
# print(res)
