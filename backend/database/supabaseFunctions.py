from backend.database import supabaseInstance
from backend.database.field import Field
from backend.database.entry import Entry

import asyncio

class supabaseFunctions:
    __sbClient = supabaseInstance.supabaseInstance().get_client()

    def __init__(self):
        pass

    @staticmethod
    def getFieldData(fieldid: str):
        try:
            dict = {"field_id": fieldid}
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
        except Exception as e:
            print(e)
            return {"error": "Failed to get field info", "error_message": e}
        finally:
            if response.data == []:
                return {"error": "Field not found. Please create a field first."}
            return response.data

    @staticmethod
    def createField(fieldInfo: Field):
        try:
            supabaseFunctions.__sbClient.table("field_info").insert([{"field_area": fieldInfo.field_area, "field_name": fieldInfo.field_name, "field_tph": fieldInfo.field_tph, "field_health": fieldInfo.field_health, "crop_type": fieldInfo.crop_type, "user_id": fieldInfo.user_id}]).execute()
        except Exception as e:
            print(e)
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
        

    # integration testing from get to post
    @staticmethod
    def test():
        testsPassed = 0
        response = None
        try:
            dict_params = {"field_id": 0}
            response = supabaseFunctions.__sbClient.rpc("get_field_info", dict_params).execute()
            if response.data == []:
                raise Exception("Field not found")
            testsPassed += 1

            dict_params = {"field_id": 0}
            response = supabaseFunctions.__sbClient.rpc("get_field_data_by_id", dict_params).execute()
            if response.data == []:
                raise Exception("Data not found")
            testsPassed += 1
            
            dict_params = {"entry_id": "0", "weather_temperature": 30, "weather_humidity": 50, "weather_uv": 5, "weather_rainfall": 0, "soil_moisture": 50, "soil_ph": 6, "soil_conductivity": 0, "is_manual": False, "field_id": 0}

            response = supabaseFunctions.__sbClient.table("data_feed").insert([dict_params]).execute()

            # see if entry was created
            dict_params = {"entry_id": "0"}
            # response = supabaseFunctions.__sbClient.table("data_feed").select().eq("entry_id", dict_params.get("entry_id")).execute()

            # asyncio.sleep(5)

            # print(response.data, flush=True)
            # if response.data == []:
            #     raise Exception("Entry not created")
            testsPassed += 1

            dict_params = {"entry_id": "0", "weather_temperature": 30, "weather_humidity": 50, "weather_uv": 5, "weather_rainfall": 0, "soil_moisture": 50, "soil_ph": 6, "soil_conductivity": 0, "is_manual": True, "field_id": 0}

            response = supabaseFunctions.__sbClient.table("data_feed").update(dict_params).eq("entry_id", dict_params.get("entry_id")).execute()

            # see if entry was updated
            # dict_params = {"entry_id": "0"}
            # response = supabaseFunctions.__sbClient.table("data_feed").select().eq("entry_id", dict_params.get("entry_id")).execute()
            # if response.data[0]["is_manual"] != True:
            #     raise Exception("Entry not updated")
            testsPassed += 1

            dict_params = {"entry_id": "0"}

            response = supabaseFunctions.__sbClient.table("data_feed").delete().eq("entry_id", dict_params.get("entry_id")).execute()

            # see if entry was deleted
            # dict_params = {"entry_id": "0"}
            # response = supabaseFunctions.__sbClient.table("data_feed").select().eq("entry_id", dict_params.get("entry_id")).execute()
            # if response.data != []:
            #     raise Exception("Entry not deleted")
            testsPassed += 1

            # see if entry is still there
            dict_params = {"entry_id": "0"}
            response = supabaseFunctions.__sbClient.table("data_feed").select().eq("entry_id", dict_params.get("entry_id")).execute()

            if response.data != []:
                raise Exception("Entry not deleted")

            
            dict_params = {"id": 1, "field_area": 100, "field_name": "Test Field", "field_tph": 6, "field_health": 5, "crop_type": "Rice", "team_id": "592a7e6e-85f7-4830-8f1a-d2f396353a4b"}
            supabaseFunctions.__sbClient.table("field_info").insert([dict_params]).execute()
            testsPassed += 1
            supabaseFunctions.__sbClient.table("field_info").update({"field_area": 200}).eq("id", 1).execute()
            testsPassed += 1
            supabaseFunctions.__sbClient.table("field_info").delete().eq("id", 1).execute()
            testsPassed += 1

            dict_params = {"field_id": 1}
            response = supabaseFunctions.__sbClient.rpc("get_field_info", dict_params).execute()

            if response.data != []:
                raise Exception("Entry not deleted")

            return {"success": "All tests passed", "tests_passed": testsPassed}
        
        except Exception as e:
            print(e)
            return {"error": "Test failed", "error_message": str(e)}
    
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