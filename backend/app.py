import json
from backend.model.base import initModel
from fastapi import FastAPI
# from backend.database.supabaseFunctions import signUp, login, logout, getUser
from backend.database.supabaseFunctions import sbGetFieldInfo, sbGetFieldData, sbCreateField, sbUpdateField, sbDeleteField, sbCreateEntry, sbUpdateEntry, sbDeleteEntry
from pydantic import BaseModel
app = FastAPI()

# base model
class Field(BaseModel):
    field_area: object
    field_name: str
    field_tph: float
    field_health: float
    crop_type: str
    user_id: str

@app.get("/")
def main():
    return initModel()

@app.get("/getFieldInfo")
def getFieldInfo():
    return sbGetFieldInfo()

@app.get("/getFieldData/{fieldid}")
def getFieldData(fieldid: int):
    return sbGetFieldData(fieldid)

@app.post("/createField")
def createField(fieldInfo: Field):
    # print("createField")
    # print(fieldInfo.field_area)
    return sbCreateField(fieldInfo.field_area, fieldInfo.field_name, fieldInfo.field_tph, fieldInfo.field_health, fieldInfo.crop_type, fieldInfo.user_id)

# update type of field for example
@app.post("/updateField")
def updateField(field_id: int, field_area: object, field_name: str, field_tph: float, field_health: float, crop_type: str, user_id: int):
    return sbUpdateField(field_id)


# @app.post("/deleteField")

# @app.post("/createEntry")

# # update data
# @app.post("/updateEntry")

# @app.post("/deleteEntry")



# @app.get("/getFieldInfo")
# def getFieldInfo():
#     return sbGetFieldInfo()


# # sign up user
# @app.post("/signUpUser")
# def signUpUser(user: dict):
#     return signUp(user)

# # login user
# @app.post("/loginUser")
# def loginUser(user: dict):
#     return login(user)

# # get user info
# @app.post("/getUser")
# def getUserInfo():
#     return getUser()

# #logout user
# @app.post("/logoutUser")
# def logoutUser():
#     return logout()