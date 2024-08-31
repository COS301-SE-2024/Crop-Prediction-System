import getNewSensorData from './getData.py'
import createUpSensorData from '../database/supabaseFunctions.py'

def storeSensorData(sensorID: str, number_of_rows: int = 1):
    # get the data from the sensor api
    data = getNewSensorData(sensorID, number_of_rows)
    # store the data in the database
    # need to change to api call?
    createUpSensorData(data)
