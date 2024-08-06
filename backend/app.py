from datetime import date
import uuid
from fastapi import FastAPI, Request
from database.supabaseFunctions import supabaseFunctions
from pydantic import BaseModel

from model.model import Model
from definitions.field import Field
from definitions.entry import Entry
from functools import wraps

class API:
    def __init__(self):
        self.app = FastAPI()
        self.sb = supabaseFunctions()
        self.ml = Model(sb=self.sb)
        self.setup_routes()

    def setup_routes(self):
        self.app.add_api_route("/", self.main, methods=["GET"])

        # field routes
        self.app.add_api_route("/getFieldInfo", self.getFieldInfo, methods=["GET"])
        self.app.add_api_route("/getFieldData", self.getFieldData, methods=["GET"])
        # self.app.add_api_route("/getFieldLogs", self.getFieldLogs, methods=["GET"])
        self.app.add_api_route("/fetchWeather", self.sb.fetchWeatherForAllFields, methods=["GET"])

        # field routes
        self.app.add_api_route("/createField", self.createField, methods=["POST"])
        self.app.add_api_route("/updateField", self.updateField, methods=["PUT"])
        self.app.add_api_route("/deleteField", self.deleteField, methods=["POST"])

        # entry routes
        # self.app.add_api_route("/createEntry", self.createEntry, methods=["POST"])
        # self.app.add_api_route("/updateEntry", self.updateEntry, methods=["PUT"])
        # self.app.add_api_route("/deleteEntry", self.deleteEntry, methods=["POST"])

        # user routes
        self.app.add_api_route("/getUserFields", self.getUserFields, methods=["GET"])
        self.app.add_api_route("/addToTeam", self.addToTeam, methods=["POST"])
        self.app.add_api_route("/removeFromTeam", self.removeFromTeam, methods=["GET"])
        self.app.add_api_route("/updateRoles", self.updateRoles, methods=["POST"])

        # /getTeamId
        self.app.add_api_route("/getTeamId", self.sb.getTeamId, methods=["GET"])

        # model routes
        self.app.add_api_route("/predict", self.predict, methods=["POST"])
        self.app.add_api_route("/train", self.ml.train, methods=["GET"])
                               
    def main(self, request: Request):
        return {
            "Welcome": "Welcome to the TerraByte API",
            "Link to Documentation": "https://documenter.getpostman.com/view/26558432/2sA3Qwaoyd"
        }

    def getFieldInfo(self, request: Request, fieldid: uuid):
        return self.sb.getFieldInfo(str(fieldid))

    def getFieldData(self, request: Request, fieldid: uuid, input_date: date):
        return self.sb.getFieldData(str(fieldid))

    def createField(self, request: Request, fieldInfo: Field):
        return self.sb.createField(fieldInfo)

    def updateField(self, request: Request, fieldInfo: Field):
        return self.sb.updateField(fieldInfo)

    def deleteField(self, request: Request, field_id: dict):
        return self.sb.deleteField(field_id.get("field_id"))

    # entry routes
    def createEntry(self, request: Request, entryInfo: Entry):
        return self.sb.createEntry(entryInfo)

    def updateEntry(self, request: Request, entryInfo: Entry):
        return self.sb.updateEntry(entryInfo)

    def deleteEntry(self, request: Request, entry_id: dict):
        return self.sb.deleteEntry(entry_id.get("entry_id"))

    def getUserFields(self, request: Request, userid: str):
        return self.sb.getUserFields(userid)

    # team routes
    def addToTeam(self, request: Request, team: dict):
        return self.sb.addToTeam(team)
    
    def removeFromTeam(self, request: Request, user_id: str):
        return self.sb.removeFromTeam(user_id)

    def updateRoles(self, request: Request, user: dict):
        return self.sb.updateRoles(user)

    def getTeamId(self, request: Request, user_id: str):
        return self.sb.getTeamId(user_id)
    
    # model routes
    def predict(self, request: Request, data: dict):
        return self.ml.predict(data.get("data"), data.get("crop"), data.get("hectare"))

api_instance = API()
app = api_instance.app
