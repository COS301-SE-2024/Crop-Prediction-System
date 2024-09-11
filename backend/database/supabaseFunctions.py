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

class supabaseFunctions:
    __sbClient = supabaseInstance.supabaseInstance().get_client()
    weather = Weather()
    agg = Aggregate()
    
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
    def updateEntry(fieldData: Entry):
        try:
            response = supabaseFunctions.__sbClient.table("field_data").update(fieldData).eq("entry_id", fieldData.id).execute()
            if response.error:
                raise Exception(response.error)
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