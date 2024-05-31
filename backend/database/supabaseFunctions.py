from backend.database import supabaseInstance
from backend.database.field import Field
from backend.database.entry import Entry

class supabaseFunctions:
    __sbClient = supabaseInstance.supabaseInstance().get_client()

    def __init__(self):
        pass

    @staticmethod
    def getFieldData(fieldid: str):
        try:
            dict = {"fieldid": fieldid}
            response = supabaseFunctions.__sbClient.rpc("get_field_data_by_id", dict).execute()
        except Exception as e:
            print(e)
            return {"error": "Failed to get field data"}
        finally:
            if response.data == []:
                return {"error": "Data not found. Field ID may be invalid or may not have any data."}
            return response.data

    @staticmethod
    def getFieldInfo(fieldid: str):
        try:
            dict = {"field_id": fieldid}
            response = supabaseFunctions.__sbClient.rpc("get_field_info", dict).execute()
        except Exception as e:
            print(e)
            return {"error": "Failed to get field info"}
        finally:
            if response.data == []:
                return {"error": "Field not found. Please create a field first."}
            return response.data

    @staticmethod
    def createField(fieldInfo: Field):
        if fieldInfo.user_id == "":
            try:
                supabaseFunctions.__sbClient.table("field_info").insert([{"field_area": fieldInfo.field_area, "field_name": fieldInfo.field_name, "field_tph": fieldInfo.field_tph, "field_health": fieldInfo.field_health, "crop_type": fieldInfo.crop_type}]).execute()
            except Exception as e:
                print(e)
                return {"error": "Failed to create field"}
            finally:
                return {"success": "Field created"}
        try:
            supabaseFunctions.__sbClient.table("field_info").insert([{"field_area": fieldInfo.field_area, "field_name": fieldInfo.field_name, "field_tph": fieldInfo.field_tph, "field_health": fieldInfo.field_health, "crop_type": fieldInfo.crop_type, "user_id": fieldInfo.user_id}]).execute()
        except Exception as e:
            print(e)
            return {"error": "Failed to create field"}
        finally:
            return {"success": "Field created"}

    @staticmethod
    def updateField(fieldInfo: Field):
        try:
            supabaseFunctions.__sbClient.table("field_info").update({"field_area": fieldInfo.field_area, "field_name": fieldInfo.field_name, "field_tph": fieldInfo.field_tph, "field_health": fieldInfo.field_health, "crop_type": fieldInfo.crop_type, "user_id": fieldInfo.user_id}).eq("field_id", fieldInfo.field_id).execute()
        except Exception as e:
            print(e)
            return {"error": "Field not found"}
        finally:
            return {"success": "Field updated"}
        
    @staticmethod
    def deleteField(field_id: int):
        try:
            supabaseFunctions.__sbClient.table("field_info").delete().eq("field_id", field_id).execute()
        except Exception as e:
            print(e)
            return {"error": "Field not found"}
        finally:
            return {"success": "Field deleted"}
    
    @staticmethod
    def createEntry(fieldData: Entry):
        try:
            supabaseFunctions.__sbClient.table("field_data").insert([{"weather_temperature": fieldData.weather_temperature, "weather_humidity": fieldData.weather_humidity, "weather_uv": fieldData.weather_uv, "weather_rainfall": fieldData.weather_rainfall, "soil_moisture": fieldData.soil_moisture, "soil_ph": fieldData.soil_ph, "soil_conductivity": fieldData.soil_conductivity, "is_manual": fieldData.is_manual, "field_id": fieldData.field_id}]).execute()
        except Exception as e:
            print(e)
            return {"error": "Failed to create entry"}
        finally:
            return {"success": "Entry created"}
        
    @staticmethod
    def updateEntry(fieldData: Entry):
        try:
            supabaseFunctions.__sbClient.table("field_data").update({"weather_temperature": fieldData.weather_temperature, "weather_humidity": fieldData.weather_humidity, "weather_uv": fieldData.weather_uv, "weather_rainfall": fieldData.weather_rainfall, "soil_moisture": fieldData.soil_moisture, "soil_ph": fieldData.soil_ph, "soil_conductivity": fieldData.soil_conductivity, "is_manual": fieldData.is_manual, "field_id": fieldData.field_id}).eq("entry_id", fieldData.entry_id).execute()
        except Exception as e:
            print(e)
            return {"error": "Entry not found"}
        finally:
            return {"success": "Entry updated"}
        
    @staticmethod
    def deleteEntry(entry_id: int):
        try:
            supabaseFunctions.__sbClient.table("field_data").delete().eq("entry_id", entry_id).execute()
        except Exception as e:
            print(e)
            return {"error": "Entry not found"}
        finally:
            return {"success": "Entry deleted"}
        

# __sbClient = supabaseInstance.supabaseInstance().get_client()

# def getFieldData(fieldid: str):
#     try:
#         dict = {"fieldid": fieldid}
#         response = __sbClient.rpc("get_field_data_by_id", dict).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Failed to get field data"}
#     finally:
#         if response.data == []:
#             return {"error": "Data not found. Field ID may be invalid or may not have any data."}
#         return response.data

# def getFieldInfo(fieldid: str):
#     try:
#         dict = {"field_id": fieldid}
#         response = __sbClient.rpc("get_field_info", dict).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Failed to get field info"}
#     finally:
#         if response.data == []:
#             return {"error": "Field not found. Please create a field first."}
#         return response.data

# def createField(field_area, field_name: str, field_tph: float, field_health: float, crop_type: str, user_id: str):
#     if user_id == "":
#         try:
#             __sbClient.table("field_info").insert([{"field_area": field_area, "field_name": field_name, "field_tph": field_tph, "field_health": field_health, "crop_type": crop_type}]).execute()
#         except Exception as e:
#             print(e)
#             return {"error": "Failed to create field"}
#         finally:
#             return {"success": "Field created"}
#     try:
#         __sbClient.table("field_info").insert([{"field_area": field_area, "field_name": field_name, "field_tph": field_tph, "field_health": field_health, "crop_type": crop_type, "user_id": user_id}]).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Failed to create field"}
#     finally:
#         return {"success": "Field created"}

# def updateField(field_id: int, field_area: object, field_name: str, field_tph: float, field_health: float, crop_type: str, user_id: int):
#     try:
#         __sbClient.table("field_info").update({"field_area": field_area, "field_name": field_name, "field_tph": field_tph, "field_health": field_health, "crop_type": crop_type, "user_id": user_id}).eq("field_id", field_id).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Field not found"}
#     finally:
#         return {"success": "Field updated"}

# def deleteField(field_id: int):
#     try:
#         __sbClient.table("field_info").delete().eq("field_id", field_id).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Field not found"}
#     finally:
#         return {"success": "Field deleted"}

# def createEntry(weather_temperature: float, weather_humidity: float, weather_uv: float, weather_rainfall: float, soil_moisture: float, soil_ph:float, soil_conductivity: float, is_manual: bool, field_id: int):
#     try:
#         __sbClient.table("field_data").insert([{"weather_temperature": weather_temperature, "weather_humidity": weather_humidity, "weather_uv": weather_uv, "weather_rainfall": weather_rainfall, "soil_moisture": soil_moisture, "soil_ph": soil_ph, "soil_conductivity": soil_conductivity, "is_manual": is_manual, "field_id": field_id}]).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Failed to create entry"}
#     finally:
#         return {"success": "Entry created"}

# def updateEntry(entry_id: int, weather_temperature: float, weather_humidity: float, weather_uv: float, weather_rainfall: float, soil_moisture: float, soil_ph:float, soil_conductivity: float, is_manual: bool, field_id: int):
#     try:
#         __sbClient.table("field_data").update({"weather_temperature": weather_temperature, "weather_humidity": weather_humidity, "weather_uv": weather_uv, "weather_rainfall": weather_rainfall, "soil_moisture": soil_moisture, "soil_ph": soil_ph, "soil_conductivity": soil_conductivity, "is_manual": is_manual, "field_id": field_id}).eq("entry_id", entry_id).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Entry not found"}
#     finally:
#         return {"success": "Entry updated"}

# def deleteEntry(entry_id: int):
#     try:
#         __sbClient.table("field_data").delete().eq("entry_id", entry_id).execute()
#     except Exception as e:
#         print(e)
#         return {"error": "Entry not found"}
#     finally:
#         return {"success": "Entry deleted"}