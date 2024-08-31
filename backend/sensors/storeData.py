import getNewSensorData from './getData.py'
import createUpSensorData from '../database/supabaseFunctions.py'

def storeSensorData(sensorID):
    # get the data from the sensor api
    data = getNewSensorData(sensorID)
    # store the data in the database
    # need to change to api call?
    createUpSensorData(data)
