from datetime import date
import uuid
from database import supabaseInstance
from definitions.field import Field
from definitions.entry import Entry
from definitions.crop import Crop
from logic.weather import Weather
from logic.calculateHectare import calculate_hectares_from_coordinates
from logic.aggregate import Aggregate
import datetime
from collections import defaultdict

class supabaseFunctions:
    __sbClient = supabaseInstance.supabaseInstance().get_client()
    weather = Weather()
    agg = Aggregate()
    
    def __init__(self):
        pass

    @staticmethod
    def getCrop(crop_type: str):
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
            print(e)
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
    def getCurrentStage(c : Crop):
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
    def aggregate():
        try:
            # Fetch fields
            response = supabaseFunctions.__sbClient.table("field_info").select("*").execute()
            if response.data == []:
                return {"error": "Data not found. Please create a field first."}

            # Dictionary to accumulate entries by field and stage
            entries_by_field_stage = defaultdict(lambda: defaultdict(list))

            for field in response.data:
                # Get all entries for each field
                response2 = supabaseFunctions.__sbClient.table("field_data").select("*").eq("field_id", field["id"]).execute()
                if response2.data == []:
                    return {"error": "Data not found. Please create an entry first."}
                
                for entry in response2.data:
                    # Get crop info
                    c = supabaseFunctions.getCrop(field["crop_type"])

                    # Determine current stage
                    stage = supabaseFunctions.getCurrentStage(c)

                    # Build an Entry object
                    e = Entry(
                        field_id=field["id"],
                        timestamp=datetime.datetime.strptime(entry["date"], "%Y-%m-%d").timestamp(),
                        summary=entry["summary"],
                        tempMax=entry["tempmax"],
                        tempMin=entry["tempmin"],
                        tempDiurnal=entry["tempdiurnal"],
                        tempMean=entry["tempmean"],
                        pressure=entry["pressure"],
                        humidity=entry["humidity"],
                        dew_point=entry["dew_point"],
                        wind_speed=entry["wind_speed"],
                        wind_deg=entry["wind_deg"],
                        wind_gust=entry["wind_gust"],
                        clouds=entry["clouds"],
                        pop=entry["pop"],
                        rain=entry["rain"],
                        uvi=entry["uvi"],
                        gff=entry["gff"],
                        gdd=entry["gdd"],
                        hdd=entry["hdd"],
                        soil_moisture=entry["soil_moisture"],
                        soil_temperature=entry["soil_temperature"],
                        pet=entry["pet"]
                    )

                    # Accumulate entries by field and stage
                    if stage:
                        entries_by_field_stage[field["id"]][stage].append(e)

            # Aggregate data for each field and stage
            for field_id, stages in entries_by_field_stage.items():
                for stage, entries in stages.items():
                    supabaseFunctions.agg.aggregate(entries, stage, field_id)
                    print(f"Aggregated data for field {field_id}, stage {stage}", flush=True)

            return {"success": "Aggregated data for all fields"}
        except Exception as e:
            print(e)
            return {"error": "Failed to aggregate data", "error_message": str(e)}

    @staticmethod
    def getFieldData(fieldid: str, input_date: str):
        try:
            dict = {"fieldid": fieldid, "input_date": input_date}
            response = supabaseFunctions.__sbClient.rpc("get_field_data_by_id", dict).execute()
            if response.data == []:
                return {"error": "Data not found. Field ID may be invalid or may not have any data."}
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get field data", "error_message": e}

    @staticmethod
    def getFieldInfo(fieldid: str):
        try:
            dict = {"field_id": fieldid}
            response = supabaseFunctions.__sbClient.rpc("get_field_info", dict).execute()
            return response.data[0]
        except Exception as e:
            print(e)
            return {"error": "Failed to get field info", "error_message": e}
        
    def getUserFieldData(self, userid: str, n: int):
        try:
            dict = {"userid": userid}
            team = supabaseFunctions.__sbClient.rpc("get_team_id", dict).execute()
            if team.data != []:
                dict = {"teamid": team.data[0]["team_id"]}
                response = supabaseFunctions.__sbClient.rpc("get_data_from_team", dict).execute()
                if response.data == []:
                    return {"error": "Data not found. User ID may be invalid or may not have any data."}
                
                # sort entries by date
                response.data = sorted(response.data, key=lambda x: x["date"])
                
                # return the last n entries
                if n > 0:
                    return response.data[-n:]
                return response.data
            else:
                return {"error": "User not found"}
        except Exception as e:
            return {"error": "Failed to get user field data", "error_message": e}

    @staticmethod
    def createField(fieldInfo: Field):
        try:
            array = fieldInfo.field_area['coordinates']

            fieldid = uuid.uuid4()
            fieldid = str(fieldid)

            array = [tuple(i) for i in array]
            hectare = calculate_hectares_from_coordinates(array)

            result = supabaseFunctions.__sbClient.table("field_info").insert([{"id": fieldid, "field_area": array, "field_name": fieldInfo.field_name, "crop_type": fieldInfo.crop_type, "team_id": fieldInfo.team_id, "hectare": hectare}]).execute()

            c = supabaseFunctions.getCrop(fieldInfo.crop_type)
            w = supabaseFunctions.weather.getWeather(array[0][0], array[0][1], fieldid, c)
            s = supabaseFunctions.weather.getSummary(array[0][0], array[0][1], fieldid)
            # print(w, flush=True)
            
            return result.data
        except Exception as e:
            # print(e)
            return {"error": "Failed to create field", "error_message": e, "type": "createField"}
        finally:
            return {"success": "Field created"}

    @staticmethod
    def updateField(fieldInfo: Field):
        try:
            if fieldInfo.field_id is None:
                return {"error": "Field ID is required"}
            
            # print(f"Updating field with ID: {fieldInfo.field_id}", flush=True)
            
            # dict = {"field_id": fieldInfo.field_id}
            # print(dict, flush=True)
            # print(dict.get("field_id"), flush=True)
            # isField = supabaseFunctions.__sbClient.table("field_info").select().eq("id", dict.get("field_id")).execute()
            # print(isField.data, flush=True)
            # if isField.data == []:
            #     return {"error": "Field not found", "field_id": fieldInfo.field_id, "type": "updateField"}
            
            fields = {}
            if fieldInfo.field_area is not None:
                fields["field_area"] = fieldInfo.field_area
            if fieldInfo.field_name is not None:
                fields["field_name"] = fieldInfo.field_name
            if fieldInfo.field_tph is not None:
                fields["field_tph"] = fieldInfo.field_tph
            if fieldInfo.field_health is not None:
                fields["field_health"] = fieldInfo.field_health
            if fieldInfo.crop_type is not None:
                fields["crop_type"] = fieldInfo.crop_type
            if fieldInfo.user_id is not None:
                fields["user_id"] = fieldInfo.user_id
            supabaseFunctions.__sbClient.table("field_info").update(fields).eq("id", fieldInfo.field_id).execute()
            return {"success": "Field updated"}
        except Exception as e:
            print(e)
            return {"error": "Field not found", "error_message": e, "id": fieldInfo.field_id, "type": "updateField"}
        
    @staticmethod
    def deleteField(field_id: int):
        try:
            if field_id is None:
                return {"error": "Field ID is required"}
            
            # isField = supabaseFunctions.__sbClient.table("field_info").select().eq("id", field_id).execute()
            # if isField.data == []:
            #     return {"error": "Field not found", "field_id": field_id, "type": "deleteField"}
            
            supabaseFunctions.__sbClient.table("field_info").delete().eq("id", field_id).execute()
            return {"success": "Field deleted"}
        except Exception as e:
            print(e)
            return {"error": "Field not found", "error_message": e, "id": field_id, "type": "deleteField"}
    
    @staticmethod
    def createEntry(fieldData: Entry):
        try:
            supabaseFunctions.__sbClient.table("data_feed").insert([{"entry_id": fieldData.entry_id, "weather_temperature": fieldData.weather_temperature, "weather_humidity": fieldData.weather_humidity, "weather_uv": fieldData.weather_uv, "weather_rainfall": fieldData.weather_rainfall, "soil_moisture": fieldData.soil_moisture, "soil_ph": fieldData.soil_ph, "soil_conductivity": fieldData.soil_conductivity, "is_manual": fieldData.is_manual, "field_id": fieldData.field_id}]).execute()
        except Exception as e:
            print(e)
            return {"error": "Failed to create entry", "error_message": e, "type": "createEntry"}
        finally:
            return {"success": "Entry created"}
        
    @staticmethod
    def updateEntry(fieldData: Entry):
        try:
            if fieldData.entry_id is None:
                return {"error": "Entry ID is required"}
            
            # isEntry = supabaseFunctions.__sbClient.table("data_feed").select().eq("entry_id", fieldData.entry_id).execute()
            # if isEntry.data == []:
            #     return {"error": "Entry not found", "entry_id": fieldData.entry_id, "type": "updateEntry"}
            
            fields = {}
            if fieldData.weather_temperature is not None:
                fields["weather_temperature"] = fieldData.weather_temperature
            if fieldData.weather_humidity is not None:
                fields["weather_humidity"] = fieldData.weather_humidity
            if fieldData.weather_uv is not None:
                fields["weather_uv"] = fieldData.weather_uv
            if fieldData.weather_rainfall is not None:
                fields["weather_rainfall"] = fieldData.weather_rainfall
            if fieldData.soil_moisture is not None:
                fields["soil_moisture"] = fieldData.soil_moisture
            if fieldData.soil_ph is not None:
                fields["soil_ph"] = fieldData.soil_ph
            if fieldData.soil_conductivity is not None:
                fields["soil_conductivity"] = fieldData.soil_conductivity
            if fieldData.is_manual is not None:
                fields["is_manual"] = fieldData.is_manual
            if fieldData.field_id is not None:
                fields["field_id"] = fieldData.field_id
            supabaseFunctions.__sbClient.table("data_feed").update(fields).eq("entry_id", fieldData.entry_id).execute()
            return {"success": "Entry updated"}
        except Exception as e:
            print(e)
            return {"error": "Entry not found", "error_message": e, "entry_id": fieldData.entry_id, "type": "updateEntry"}
        
    @staticmethod
    def deleteEntry(entry_id: int):
        try:
            if entry_id is None:
                return {"error": "Entry ID is required"}

            # isEntry = supabaseFunctions.__sbClient.table("data_feed").select().eq("entry_id", entry_id).execute()
            # if isEntry.data == []:
            #     return {"error": "Entry not found", "entry_id": entry_id, "type": "deleteEntry"}

            supabaseFunctions.__sbClient.table("data_feed").delete().eq("entry_id", entry_id).execute()
            return {"success": "Entry deleted"}
        except Exception as e:
            print(e)
            return {"error": "Entry not found", "error_message": e, "entry_id": entry_id, "type": "deleteEntry"}
    
    @staticmethod
    def getUserFields(user_id: str):
        # get team id from profile and pass it to getTeamFieldsHelper
        dict = {"userid": user_id}
        response = supabaseFunctions.__sbClient.rpc("get_team_id", dict).execute()
        if response.data == []:
            return {"error": "Team not found. Please create a team first."}
        # print(response.data[0]["id"])
        userid = response.data[0]["team_id"]
        dict2 = {"userid": userid}
        team_id = response.data[0]["team_id"]
        return supabaseFunctions.getTeamFieldsHelper(team_id)
        
    @staticmethod
    def getTeamFieldsHelper(team_id: str):
        try:
            dict = {"teamid": team_id}
            response = supabaseFunctions.__sbClient.rpc("get_all_fields_from_team", dict).execute()
            if response.data == []:
                return {"error": "Data not found. Team ID may be invalid or may not have any data."}
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get team fields", "error_message": e}    

    @staticmethod
    def addToTeam(team: dict):
        try:
            supabaseFunctions.__sbClient.table("profiles").update({"team_id": team.get("team_id")}).eq("id", team.get("user_id")).execute()
            return {"success": "Added to team"}
        except Exception as e:
            print(e)
            return {"error": "Failed to add user to team", "error_message": e}

    @staticmethod
    def removeFromTeam(user_id: str):
        try:
            response = supabaseFunctions.__sbClient.table("profiles").update({"team_id": None}).eq("id", user_id).execute()
            print(response)
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
            response = supabaseFunctions.__sbClient.table("profiles").select("team_id").eq("id", user_id).execute()
            if response.data == []:
                return {"error": "User not found"}
            return response.data[0]
        except Exception as e:
            print(e)
            return {"error": "Failed to get team ID", "error_message": e}
        
    @staticmethod
    def getRecentEntries(n : int):
        try:
            response = supabaseFunctions.__sbClient.rpc("get_recent_entries", {"n": n}).execute()
            if response.data == []:
                return {"error": "Data not found. Please create an entry first."}
            return response.data
        except Exception as e:
            print(e)
            return {"error": "Failed to get recent entries", "error_message": e}
        
    @staticmethod
    def createSensorData(sensor_data: dict):
        try:
            # Extract data from the provided dictionary
            nitrogen = sensor_data.get('Nitrogen')
            phosphor = sensor_data.get('Phosphor')
            potassium = sensor_data.get('Potassium')
            soil_moisture = sensor_data.get('Soil_Moisture')

            # Validate data
            if nitrogen is None or phosphor is None or potassium is None or soil_moisture is None:
                return {"error": "Missing required sensor data"}

            # Insert data into the 'field_data' table
            response = supabaseFunctions.__sbClient.table("field_data").insert({
                "Nitrogen": nitrogen,
                "Phosphor": phosphor,
                "Potassium": potassium,
                "Soil_Moisture": soil_moisture
            }).execute()

            if response.error:
                return {"error": "Failed to insert sensor data", "error_message": response.error}

            return {"success": "Sensor data inserted successfully", "data": response.data}
        except Exception as e:
            print(e)
            return {"error": "Failed to insert sensor data", "error_message": str(e)}