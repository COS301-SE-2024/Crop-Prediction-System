def calculateHealth(dFrame, crop, df):
    # Ensure crop is in title case
    crop = crop.title()

    # print(crop)
    # print(df)

    tmin = df.loc[df['Crop'] == crop, 'Tmin']
    tmax = df.loc[df['Crop'] == crop, 'Tmax']
    pmin = df.loc[df['Crop'] == crop, 'Pmin']
    pmax = df.loc[df['Crop'] == crop, 'Pmax']
    smmin = df.loc[df['Crop'] == crop, 'SMmin']
    smmax = df.loc[df['Crop'] == crop, 'SMmax']

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

    print(dFrame['health_score'])

    # Drop unnecessary columns
    dFrame.drop(columns=['temperature_score', 'precipitation_score', 'soil_moisture_score', 'nutrient_availability_score'], inplace=True)

    return dFrame
