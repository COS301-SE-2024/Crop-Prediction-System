from fastapi import FastAPI, Request, BackgroundTasks
from backend.database.supabaseFunctions import supabaseFunctions

from backend.model.model import Model
from backend.definitions.field import Field
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from fastapi.middleware.cors import CORSMiddleware

class API:
    def __init__(self):
        self.app = FastAPI()
        self.sb = supabaseFunctions()
        self.ml = Model()
        self.setup_routes()

    def setup_routes(self):
        self.app.add_api_route("/", self.main, methods=["GET"])

        # field routes
        self.app.add_api_route("/getFieldInfo", self.getFieldInfo, methods=["GET"])
        self.app.add_api_route("/getFieldData", self.getFieldData, methods=["GET"])
        # self.app.add_api_route("/getFieldLogs", self.getFieldLogs, methods=["GET"])
        self.app.add_api_route("/fetchWeather", self.fetchWeatherForAllFields, methods=["GET"])
        self.app.add_api_route("/fetchSummary", self.fetchSummary, methods=["GET"])
        

        # field routes
        self.app.add_api_route("/createField", self.createField, methods=["POST"])
        self.app.add_api_route("/updateField", self.updateField, methods=["PUT"])
        self.app.add_api_route("/deleteField", self.deleteField, methods=["POST"])

        # entry routes)
        self.app.add_api_route("/updateEntry", self.updateEntry, methods=["PUT"])

        # user routes
        self.app.add_api_route("/getTeamFields", self.getTeamFields, methods=["GET"])
        self.app.add_api_route("/getTeamFieldData", self.getTeamFieldData, methods=["GET"])
        self.app.add_api_route("/addToTeam", self.addToTeam, methods=["POST"]) # TODO: Test this route
        self.app.add_api_route("/removeFromTeam", self.removeFromTeam, methods=["PUT"]) # TODO: Test this route
        self.app.add_api_route("/updateRoles", self.updateRoles, methods=["POST"]) # TODO: Test this route
        self.app.add_api_route("/getTeamDetails", self.getTeamDetails, methods=["GET"]) # TODO: Test this route

        # /getTeamId
        self.app.add_api_route("/getTeamId", self.getTeamId, methods=["GET"]) # TODO: Test this route

        # model routes
        self.app.add_api_route("/aggregate", self.aggregate, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/predict", self.predict, methods=["GET"]) # TODO: Test this route
        self.app.add_api_route("/train", self.train, methods=["GET"]) # TODO: Test this route

        # messaging routes
        self.app.add_api_route("/sendMessage", self.sendMessage, methods=["POST"])
        self.app.add_api_route("/getTeamMessages", self.getMessages, methods=["GET"])
                               
    def main(self, request: Request):
        return {
            "Welcome": "Welcome to the TerraByte API",
            "Link to Documentation": "https://documenter.getpostman.com/view/26558432/2sA3Qwaoyd"
        }

    def getFieldInfo(self, request: Request, field_id: str):
        return self.sb.getFieldInfo(str(field_id))

    def getFieldData(self, request: Request, field_id: str, input_date: str):
        return self.sb.getFieldData(field_id, input_date)

    def createField(self, request: Request, fieldInfo: Field):
        return self.sb.createField(fieldInfo)

    def updateField(self, request: Request, fieldInfo: Field):
        return self.sb.updateField(fieldInfo)

    def deleteField(self, request: Request, field_id: dict):
        return self.sb.deleteField(field_id.get("field_id"))

    # entry routes
    def updateEntry(self, request: Request, entryInfo: Entry):
        return self.sb.updateEntry(entryInfo)

    def getTeamFields(self, request: Request, team_id: str):
        return self.sb.getTeamFields(team_id)

    # team routes
    def addToTeam(self, request: Request, team: dict):
        return self.sb.addToTeam(team)
    
    def removeFromTeam(self, request: Request, user_id: str):
        return self.sb.removeFromTeam(user_id)

    def updateRoles(self, request: Request, user: dict):
        return self.sb.updateRoles(user)

    def getTeamId(self, request: Request, user_id: str):
        return self.sb.getTeamId(user_id)
    
    def getTeamFieldData(self, request: Request, team_id: str, n : int = -1):
        return self.sb.getTeamFieldData(team_id, n)
    
    def getTeamDetails(self, request: Request, team_id: str):
        return self.sb.getTeamDetails(team_id)
    
    # model routes
    def aggregate(self, background_tasks: BackgroundTasks, request: Request):
        background_tasks.add_task(self.sb.aggregate)
        return {"message": "Started aggregation"}
    
    def predict(self, background_tasks: BackgroundTasks, request: Request, field_id: str = None, batch: bool = False):
        if batch:
            background_tasks.add_task(self.ml.predict_all)
            return {"message": "Started prediction for all fields"}
        background_tasks.add_task(self.ml.predict, field_id)
        return {"message": "Started prediction for field ID: " + field_id}
    
    def train(self, background_tasks: BackgroundTasks, request: Request, field_id: str = None, crop: str = None, batch: bool = False):
        if batch:
            background_tasks.add_task(self.ml.train_all)
            return {"message": "Started training for all fields"}
        background_tasks.add_task(self.ml.train, field_id, crop)
        return {"message": "Started training for field ID: " + field_id}
    
    def fetchWeatherForAllFields(self, background_tasks: BackgroundTasks, request: Request):
        background_tasks.add_task(self.sb.fetchWeatherForAllFields)
        return {"message": "Started fetching weather for all fields"}
    
    def fetchSummary(self, background_tasks: BackgroundTasks, request: Request):
        background_tasks.add_task(self.sb.fetchSummary)
        return {"message": "Started fetching summary"}
    
    # messaging routes
    def sendMessage(self, request: Request, content: dict):
        return self.sb.sendMessage(content)
    
    def getMessages(self, request: Request, team_id: str):
        return self.sb.getTeamMessages(team_id)

api_instance = API()
app = api_instance.app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
