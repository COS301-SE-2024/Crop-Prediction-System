from fastapi import FastAPI, Request
from database.supabaseFunctions import supabaseFunctions

from model.model import Model
from definitions.field import Field
from definitions.entry import Entry
from definitions.crop import Crop

class API:
    def __init__(self):
        self.app = FastAPI()
        self.sb = supabaseFunctions()
        self.ml = Model()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_api_route("/", self.main, methods=["GET"])

        # field routes
        self.app.add_api_route("/getFieldInfo", self.getFieldInfo, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/getFieldData", self.getFieldData, methods=["GET"]) # TODO: Test this route
        # self.app.add_api_route("/getFieldLogs", self.getFieldLogs, methods=["GET"])
        self.app.add_api_route("/fetchWeather", self.sb.fetchWeatherForAllFields, methods=["GET"])
        self.app.add_api_route("/fetchSummary", self.sb.fetchSummary, methods=["GET"])
        self.app.add_api_route("/getRecentData", self.getRecentData, methods=["GET"])
        

        # field routes
        self.app.add_api_route("/createField", self.createField, methods=["POST"]) # TODO: Test this route
        self.app.add_api_route("/updateField", self.updateField, methods=["PUT"]) # TODO: Test this route
        self.app.add_api_route("/deleteField", self.deleteField, methods=["POST"]) # TODO: Test this route

        # entry routes
        # self.app.add_api_route("/createEntry", self.createEntry, methods=["POST"])
        # self.app.add_api_route("/updateEntry", self.updateEntry, methods=["PUT"])
        # self.app.add_api_route("/deleteEntry", self.deleteEntry, methods=["POST"])

        # user routes
        self.app.add_api_route("/getUserFields", self.getUserFields, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/addToTeam", self.addToTeam, methods=["POST"]) # TODO: Test this route
        self.app.add_api_route("/removeFromTeam", self.removeFromTeam, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/updateRoles", self.updateRoles, methods=["POST"]) # TODO: Test this route

        # /getTeamId
        self.app.add_api_route("/getTeamId", self.sb.getTeamId, methods=["GET"]) # TODO: Test this route

        # model routes
        self.app.add_api_route("/aggregate", self.aggregate, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/predict", self.predict, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/train", self.train, methods=["GET"]) # TODO: Test this route
                               
    def main(self, request: Request):
        return {
            "Welcome": "Welcome to the TerraByte API",
            "Link to Documentation": "https://documenter.getpostman.com/view/26558432/2sA3Qwaoyd"
        }

    def getFieldInfo(self, request: Request, fieldid: str):
        return self.sb.getFieldInfo(str(fieldid))

    def getFieldData(self, request: Request, fieldid: str, input_date: str):
        return self.sb.getFieldData(fieldid, input_date)

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
    
    def getRecentData(self, request: Request, user_id: str, n : int = -1):
        return self.sb.getUserFieldData(user_id, n)
    
    # model routes
    def aggregate(self, request: Request):
        return self.sb.aggregate()
    
    def predict(self, request: Request, field_id: str = None, batch: bool = False):
        if batch:
            return self.ml.predict_all()
        return self.ml.predict(field_id)
    
    def train(self, request: Request, field_id: str = None, crop: str = None, batch: bool = False):
        if batch:
            return self.ml.train_all()
        return self.ml.train(field_id, crop)

api_instance = API()
app = api_instance.app
