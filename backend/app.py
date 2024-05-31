from fastapi import FastAPI
# from backend.database.supabaseFunctions import signUp, login, logout, getUser
from backend.database.supabaseFunctions import supabaseFunctions
from pydantic import BaseModel

from backend.model.base import MLModel
from backend.database.field import Field
from backend.database.entry import Entry

class API:
    def __init__(self):
        self.app = FastAPI()
        self.ml = MLModel()
        self.sb = supabaseFunctions()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_api_route("/", self.main, methods=["GET"])
        self.app.add_api_route("/startModel", self.initModel, methods=["GET"])
        self.app.add_api_route("/getFieldInfo", self.getFieldInfo, methods=["GET"])
        self.app.add_api_route("/getFieldData", self.getFieldData, methods=["GET"])
        self.app.add_api_route("/createField", self.createField, methods=["POST"])
        self.app.add_api_route("/updateField", self.updateField, methods=["POST"])
        self.app.add_api_route("/deleteField", self.deleteField, methods=["POST"])
        self.app.add_api_route("/createEntry", self.createEntry, methods=["POST"])
        self.app.add_api_route("/updateEntry", self.updateEntry, methods=["POST"])
        self.app.add_api_route("/deleteEntry", self.deleteEntry, methods=["POST"])

    def main(self):
        return {
            "Welcome": "Welcome to the TerraByte API",
            "Documentation": "Visit Postman for more information",
            "Link to Postman": "https://documenter.getpostman.com/view/12263200/TzJx9G8z"
        }

    def initModel(self):
        return self.ml.startModel()

    def getFieldInfo(self, fieldid: int = 0):
        return self.sb.getFieldInfo(str(fieldid))

    def getFieldData(self, fieldid: int = 0):
        return self.sb.getFieldData(str(fieldid))

    def createField(self, fieldInfo: Field):
        return self.sb.createField(fieldInfo)

    def updateField(self, fieldInfo: Field):
        return self.sb.updateField(fieldInfo)

    def deleteField(self, field_id: dict):
        return self.sb.deleteField(field_id)

    def createEntry(self, entryInfo: Entry):
        return self.sb.createEntry(entryInfo)

    def updateEntry(self, entryInfo: Entry):
        return self.sb.updateEntry(entryInfo)

    def deleteEntry(self, entry_id: dict):
        return self.sb.deleteEntry(entry_id)
    
api_instance = API()
app = api_instance.app