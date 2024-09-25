from datetime import date
import uuid
from backend.database import supabaseInstance
from backend.definitions.field import Field
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from backend.logic.weather import Weather
from backend.logic.calculateHectare import calculate_hectares_from_coordinates
from backend.logic.aggregate import Aggregate
import datetime
from collections import defaultdict
from backend.sensors.getData import getNewSensorData

from backend.sensors.farmerSensor import Sensor

class supabaseFunctions:
    __sbClient = supabaseInstance.supabaseInstance().get_client()
    weather = Weather()
    
    def __init__(self):
        pass

    @staticmethod
    def getCrop(crop_type: str) -> Crop:
        try:
            response = supabaseFunctions.__sbClient.table("crop_info").select("*").eq("name", crop_type).execute()
            if response.data == []:
                return {"error": "Data not found. Crop type may be invalid or may not have any data."}
            
            c = Crop(
                name = response.data[0]["name"],
                t_base = response.data[0]["t_base"],
                stages = response.data[0]["stages"]
            )

            return c
        except Exception as e:
            return {"error": "Failed to get crop", "error_message": e}
        
    @staticmethod
    def fetchWeatherForAllFields():
        try:
            response = supabaseFunctions.__sbClient.table("field_info").select("*").execute()
            if response.data == []:
                return {"error": "Data not found. Please create a field first."}
            for field in response.data:
                c = supabaseFunctions.getCrop(field["crop_type"])
                supabaseFunctions.weather.getWeather(field["field_area"][0][0], field["field_area"][0][1], field["id"], c)
            return {"success": "Weather fetched for all fields"}
        except Exception as e:
            print(e)
            return {"error": "Failed to fetch weather for all fields", "error_message": e}
        
    @staticmethod
    def fetchSummary():
        try:
            response = supabaseFunctions.__sbClient.table("field_info").select("*").execute()
            if response.data == []:
                return {"error": "Data not found. Please create a field first."}
            for field in response.data:
                supabaseFunctions.weather.getSummary(field["field_area"][0][0], field["field_area"][0][1], field["id"])
            return {"success": "Summary fetched for all fields"}
        except Exception as e:
            print(e)
            return {"error": "Failed to fetch summary for all fields", "error_message": e}
        
    @staticmethod
    def getCurrentStage(c : Crop) -> str:
        # Determine current day of the year
        today = date.today()
        day_of_year = today.timetuple().tm_yday

        # Sort stages by day before iterating
        c.stages = dict(sorted(c.stages.items(), key=lambda item: item[1]["day"]))

        # Determine the current stage
        stage = None
        for s_name, s_info in c.stages.items():
            if day_of_year >= s_info["day"]:
                stage = s_name
            else:
                break
        
        return stage

    @staticmethod
    def getFieldData(fieldid: str):
        try:
            dict = {"fieldid": fieldid}
            response = supabaseFunctions.__sbClient.rpc("get_field_data_by_id", dict).execute()
            if response.data == []:
                return {"error": "Data not found. Field ID may be invalid or may not have any data."}
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get field data", "error_message": e}

    @staticmethod
    def getFieldInfo(fieldid: str) -> Field:
        try:
            dict = {"field_id": fieldid}
            response = supabaseFunctions.__sbClient.rpc("get_field_info", dict).execute()
            
            f = Field(
                field_id = response.data[0]["id"],
                field_area = response.data[0]["field_area"],
                field_name = response.data[0]["field_name"],
                crop_type = response.data[0]["crop_type"],
                team_id = response.data[0]["team_id"],
                hectare = response.data[0]["hectare"]
            )

            return f
        except Exception as e:
            print(e)
            return {"error": "Failed to get field info", "error_message": e}
        
    def getTeamFieldData(self, team_id: str, n: int):
        try:
            dict = {"teamid": team_id}
            response = supabaseFunctions.__sbClient.rpc("get_data_from_team", dict).execute()
            if response.data == []:
                return {"error": "Data not found. Team ID may be invalid or may not have any data."}
            
            # sort entries by date
            response.data = sorted(response.data, key=lambda x: x["date"])
            
            # return the last n entries
            if n > 0:
                return response.data[-n:]
            return response.data
        except Exception as e:
            return {"error": "Failed to get user field data", "error_message": e}
        
    @staticmethod
    def getPastYieldAvg(crop: str):
        # get past yield from crop_production
        try:
            if crop == "sunflower":
                crop += "seed"
            crop += "_ton_per_hectare"
            response = supabaseFunctions.__sbClient.table("crop_production").select(crop).execute()
            if response.data == []:
                return {"error": "Data not found. Crop type may be invalid or may not have any data."}
            
            # transpose
            data = list(response.data)

            # remove None values
            data = [i for i in data if i[crop] is not None]

            # select last 5 values
            data = data[-5:]

            data = [i[crop] for i in data]

            # calculate average
            avg = sum(data) / len(data)
            return avg
        except Exception as e:
            return {"error": "Failed to get past yield average", "error_message": e}

    @staticmethod
    def createField(fieldInfo: Field):
        try:
            array = fieldInfo.field_area['coordinates']

            fieldid = fieldInfo.field_id
            if fieldid is None:
                fieldid = uuid.uuid4()
                fieldid = str(fieldid)

            array = [tuple(i) for i in array]
            hectare = calculate_hectares_from_coordinates(array)

            result = supabaseFunctions.__sbClient.table("field_info").insert([{"id": fieldid, "field_area": array, "field_name": fieldInfo.field_name, "crop_type": fieldInfo.crop_type, "team_id": fieldInfo.team_id, "hectare": hectare}], returning="representation").execute()

            c = supabaseFunctions.getCrop(fieldInfo.crop_type)
            w = supabaseFunctions.weather.getWeather(array[0][0], array[0][1], fieldid, c)
            s = supabaseFunctions.weather.getSummary(array[0][0], array[0][1], fieldid)
            # print(w, flush=True)
            if result.data == []:
                raise Exception("Failed to create field. Possibly, check duplicate keys.")
            else:
                return {
                    "status": "success",
                    "id": result.data[0]["id"],
                }
        except Exception as e:
            # print(e)
            return {"error": "Failed to create field", "error_message": e, "type": "createField"}

    @staticmethod
    def updateField(fieldInfo: Field):
        try:
            if fieldInfo.field_id is None:
                return {"error": "Field ID is required"}
            
            fields = {}
            if fieldInfo.field_area is not None:
                fields["field_area"] = fieldInfo.field_area
            if fieldInfo.field_name is not None:
                fields["field_name"] = fieldInfo.field_name
            if fieldInfo.crop_type is not None:
                fields["crop_type"] = fieldInfo.crop_type
            if fieldInfo.team_id is not None:
                fields["team_id"] = fieldInfo.team_id
            result = supabaseFunctions.__sbClient.table("field_info").update(fields).eq("id", fieldInfo.field_id).execute()

            if result.data == []:
                raise Exception("Field not found")
            else:
                return {
                    "status": "success",
                    "data": result.data[0]
                }
        except Exception as e:
            print(e)
            return {"error_message": e, "id": fieldInfo.field_id, "type": "updateField"}
        
    @staticmethod
    def deleteField(field_id: int):
        try:
            if field_id is None:
                return {"error": "Field ID is required"}
            
            result = supabaseFunctions.__sbClient.table("field_info").delete().eq("id", field_id).execute()
            if result.data == []:
                raise Exception("Field not found")
            else:
                return {
                    "status": "success",
                    "data": result.data[0]
                }
        except Exception as e:
            print(e)
            return {"error_message": e, "id": field_id, "type": "deleteField"}
        
    @staticmethod
    def updateEntry(fieldData: dict):
        try:
            print(fieldData, flush=True)

            # response = supabaseFunctions.__sbClient.table("field_data").update(fieldData).eq("field_id", fieldData["field_id"]).eq("date", fieldData["date"]).execute()

            response = supabaseFunctions.__sbClient.table("data").update(fieldData).eq("field_id", fieldData["field_id"]).eq("date", fieldData["date"]).execute()
            
            print(response, flush=True)
            
            return {
                "status": "success",
                "data": response.data[0]
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": e
            }
        
    @staticmethod
    def getTeamFields(team_id: str):
        try:
            dict = {"teamid": team_id}
            response = supabaseFunctions.__sbClient.rpc("get_all_fields_from_team", dict).execute()
            if response.data == []:
                return {"error": "Data not found. Team ID may be invalid or may not have any fields."}
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get team fields", "error_message": e}    

    @staticmethod
    def addToTeam(team: dict):
        try:
            supabaseFunctions.__sbClient.table("profiles").update(
                {
                    "team_id": team.get("team_id"),
                    "role": team.get("role")
                }).eq("id", team.get("user_id")).execute()
            return {"success": "Added to team"}
        except Exception as e:
            print(e)
            return {"error": "Failed to add user to team", "error_message": e}

    @staticmethod
    def removeFromTeam(user_id: str):
        try:
            response = supabaseFunctions.__sbClient.rpc("remove_from_team", {"user_id": user_id}).execute()
            return {"success": "Removed from team"}
        except Exception as e:
            print(e)
            return {"error": "Failed to remove from team", "error_message": e}
        
    @staticmethod
    def updateRoles(user: dict):
        try:
            supabaseFunctions.__sbClient.table("profiles").update({"role": user.get("role")}).eq("id", user.get("user_id")).execute()
            return {"success": "Updated roles"}
        except Exception as e:
            print(e)
            return {"error": "Failed to update roles", "error_message": e}
        
    @staticmethod
    def getTeamId(user_id: str):
        try:
            response = supabaseFunctions.__sbClient.table("profiles").select("team_id, role").eq("id", user_id).execute()
            if response.data == []:
                raise Exception("User not found")
            return response.data[0]
        except Exception as e:
            print(e)
            return {"error": "Failed to get team ID", "error_message": e}
        
    @staticmethod
    def getTeamDetails(team_id: str):
        try:
            response = supabaseFunctions.__sbClient.table("profiles").select("id, full_name, email, role").eq("team_id", team_id).execute()
            if response.data == []:
                raise Exception("Team not found")
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get team details", "error_message": e}
        
    @staticmethod
    def sendMessage(content: dict):
        try:
            response = supabaseFunctions.__sbClient.table("team_chat").insert([content]).execute()
            if response.data == []:
                raise Exception("Failed to send message")
            return {"success": "Message sent"}
        except Exception as e:
            print(e)
            return {"error": "Failed to send message", "error_message": e}
        
    @staticmethod
    def getTeamMessages(team_id: str):
        try:
            response = supabaseFunctions.__sbClient.table("team_chat").select("*").eq("team_id", team_id).order("created_at").execute()

            if response.data == []:
                return {"error": "No messages found for this team"}
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get team messages", "error_message": e}
        
    @staticmethod
    def updateUser(user: dict):
        try:
            response = supabaseFunctions.__sbClient.table("profiles").update(user).eq("id", user.get("id")).execute()
            if response.data == []:
                raise Exception("Failed to update user")
            return {"success": "User updated"}
        except Exception as e:
            print(e)
            return {"error": "Failed to update user", "error_message": e}
        
    @staticmethod
    def getUser(user_id: str):
        try:
            response = supabaseFunctions.__sbClient.table("profiles").select("*").eq("id", user_id).execute()
            if response.data == []:
                raise Exception("User not found")
            return response.data[0]
        except Exception as e:
            print(e)
            return {"error": "Failed to get user", "error_message": e}
        
    @staticmethod
    def getTeamYield(team_id: str):
        try:
            dict = {"teamid": team_id}
            response = supabaseFunctions.__sbClient.rpc("get_distinct_crop_yield_by_team", dict).execute()
            if response.data == []:
                return {"error": "Data not found. Team ID may be invalid or may not have any data."}
            return response.data
        except Exception as e:
            return {"error": "Failed to get team yield", "error_message": e}

    @staticmethod
    def createUpSensorData(sensorID: str):
        try:
            sensor_data = getNewSensorData(sensorID, 1)
            # Extract soil_temperature, soil_moisture, temperature, relative_humidity, received_at from the dictionary
            row = sensor_data['data']['queryTable']['rows'][0]
            values = {column['key']: column['value'] for column in row['columns']}
            device_eui = values.get('device_eui')
            soil_temperature = values.get('soil_temperature')
            soil_moisture = values.get('soil_moisture')
            temperature = values.get('temperature')
            relative_humidity = values.get('relative_humidity')
            battery = values.get('battery')
            received_at = values.get('received_at')
            print(device_eui, soil_temperature, soil_moisture, temperature, relative_humidity, battery, received_at)
            response = supabaseFunctions.__sbClient.table("up_sensor_data").insert({
                "device_eui": device_eui,
                "soil_temperature": soil_temperature,
                "soil_moisture": soil_moisture,
                "temperature": temperature,
                "relative_humidity": relative_humidity,
                "battery": battery,
                "received_at": received_at
            }).execute() 
            if response.error:
                return {"error": "Failed to insert sensor data", "error_message": response.error}
            return {"success": "Sensor data inserted successfully", "data": response.data}
        except Exception as e:
            print(e)
            return {"error": "Failed to insert sensor data", "error_message": str(e)}
        

    # add a field to a sensor
    @staticmethod
    def addFieldToSensor(sensorID: str, fieldID: str):
        try:
            response = supabaseFunctions.__sbClient.table("up_sensor_data").update({"field_id": fieldID}).eq("device_eui", sensorID).execute()
            if response.error:
                return {"error": "Failed to add field to sensor", "error_message": response.error}
            return {"success": "Field added to sensor", "data": response.data}
        except Exception as e:
            print(e)
            return {"error": "Failed to add field to sensor", "error_message": str(e)}
    
    @staticmethod    
    def createSensor(self, sensorID: str = None):
        try:
            response = supabaseFunctions.__sbClient.table("up_sensor_data").insert({"device_eui": sensorID}).execute()
            if response.error:
                return {"error": "Failed to create sensor", "error_message": response.error}
            return {"success": "Sensor created successfully", "data": response.data}
        except Exception as e:
            print(e)
            return {"error": "Failed to create sensor", "error_message": str(e)}

    @staticmethod
    def getFarmerSensorData(fieldID:str,sensorID: str):
        try:
            data = Sensor().get_all_data()
            now = datetime.datetime.now()
            response = supabaseFunctions.__sbClient.table("iot_sensor_data").insert({"field_id": fieldID, "soil_moisture":data["humidity"],"received_at": now,"soil_temperature": data["temperature"],"conductivity": data["conductivity"],"ph_value": data["ph"],"nitrogen_content": data["nitrogen"],"phosphorus_content": data["phosphorus"],"potassium_content": data["potassium"],"sensor_id": sensorID}).execute()
            if response.error:
                return {"error": "Failed to get sensor data", "error_message": response.error}
            return {"success": "Sensor data fetched successfully", "data": response.data}
        except Exception as e:
            print(e)
            return {"error": "Failed to get sensor data", "error_message": str(e)}
        
    @staticmethod
    def addFieldFarmerSensor(fieldID: str, sensorID: str):
        try:
            response = supabaseFunctions.__sbClient.table("iot_sensor_data").update({"field_id": fieldID}).eq("sensor_id", sensorID).execute()
            if response.error:
                return {"error": "Failed to add sensor to field", "error_message": response.error}
            return {"success": "Sensor added to field", "data": response.data}
        except Exception as e:
            print(e)
            return {"error": "Failed to add sensor to field", "error_message": str(e)}
            