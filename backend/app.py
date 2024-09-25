from fastapi import FastAPI, Request, BackgroundTasks
from backend.database.supabaseFunctions import supabaseFunctions

from backend.model.pipeline import Pipeline
from backend.definitions.field import Field
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
from backend.database.market import market
from fastapi.middleware.cors import CORSMiddleware

class API:
    def __init__(self):
        self.app = FastAPI()
        self.sb = supabaseFunctions()
        self.pipeline = Pipeline()
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
        self.app.add_api_route("/getPastYieldAvg", self.getPastYieldAvg, methods=["GET"])

        # team routes
        self.app.add_api_route("/getTeamFields", self.getTeamFields, methods=["GET"])
        self.app.add_api_route("/getTeamFieldData", self.getTeamFieldData, methods=["GET"])
        self.app.add_api_route("/addToTeam", self.addToTeam, methods=["POST"]) # TODO: Test this route
        self.app.add_api_route("/removeFromTeam", self.removeFromTeam, methods=["PUT"]) # TODO: Test this route
        self.app.add_api_route("/updateRoles", self.updateRoles, methods=["POST"]) # TODO: Test this route
        self.app.add_api_route("/getTeamDetails", self.getTeamDetails, methods=["GET"]) # TODO: Test this route

        # /getTeamId
        self.app.add_api_route("/getTeamId", self.getTeamId, methods=["GET"]) # TODO: Test this route

        # model routes
        # Aggregation, preparing, training and predicting the model all happens in the pipeline
        self.app.add_api_route("/train", self.train, methods=["POST"]) # TODO: Test this route

        # messaging routes
        self.app.add_api_route("/sendMessage", self.sendMessage, methods=["POST"])
        self.app.add_api_route("/getTeamMessages", self.getMessages, methods=["GET"])

        # user routes
        self.app.add_api_route("/updateUser", self.sb.updateUser, methods=["PUT"])
        self.app.add_api_route("/getUser", self.sb.getUser, methods=["GET"])

        # market API
        self.app.add_api_route("/market", self.market, methods=["GET"])
        self.app.add_api_route("/getTeamYield", self.getTeamYield, methods=["GET"])
                               
        #sensor routes
        self.app.add_api_route("/getUPSensorData", self.getUPSensorData, methods=["GET"])
        self.app.add_api_route("/addFieldToSensor", self.addFieldToSensor, methods=["POST"])
        self.app.add_api_route("/addSensor", self.addSensor, methods=["GET"])
        self.app.add_api_route("/getFarmerSensorData", self.getFarmerSensorData, methods=["GET"])
        self.app.add_api_route("/addFieldFarmerSensor", self.addFieldFarmerSensor, methods=["POST"])

    def main(self, request: Request):
        return {
            "Welcome": "Welcome to the TerraByte API",
            "Link to Documentation": "https://documenter.getpostman.com/view/26558432/2sA3Qwaoyd"
        }

    def getFieldInfo(self, request: Request, field_id: str):
        return self.sb.getFieldInfo(str(field_id))

    def getFieldData(self, request: Request, field_id: str):
        return self.sb.getFieldData(field_id)

    def createField(self, request: Request, fieldInfo: Field):
        return self.sb.createField(fieldInfo)

    def updateField(self, request: Request, fieldInfo: Field):
        return self.sb.updateField(fieldInfo)

    def deleteField(self, request: Request, field_id: dict):
        return self.sb.deleteField(field_id.get("field_id"))

    # entry routes
    def updateEntry(self, request: Request, entryInfo: dict):
        return self.sb.updateEntry(entryInfo)
    
    def getPastYieldAvg(self, request: Request, crop: str):
        return self.sb.getPastYieldAvg(crop)

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
    
    # model routes [POST]
    def train(self, background_tasks: BackgroundTasks, request: Request, body: dict):
        field_id = body.get("field_id") or None # field_id is optional
        batch = body.get("batch") or False
        waitForCompletion = body.get("waitForCompletion") or False
        if batch:
            if waitForCompletion:
                return self.pipeline.train_all()
            background_tasks.add_task(self.pipeline.train_all)
            return {"message": "Started training for all fields"}
        if field_id is None:
            return {"error": "Field ID is required or `batch` must be set to `true`"}
        if waitForCompletion:
            return self.pipeline.train(field_id)
        background_tasks.add_task(self.pipeline.train, field_id)
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
    
    # user routes
    def updateUser(self, request: Request, user: dict):
        return self.sb.updateUser(user)
    
    def getUser(self, request: Request, user_id: str):
        return self.sb.getUser(user_id)
    
    # market API
    def market(self, crop: str):
        # get the query parameters
        function = crop

        # convert function to uppercase
        function = function.upper()
        
        return market(function)
    
    def getTeamYield(self, request: Request, team_id: str):
        return self.sb.getTeamYield(team_id)

    # sensor routes
    def getUPSensorData(self, request: Request, sensorID: str):
        return self.sb.createUpSensorData(sensorID)
    
    def addFieldToSensor(self, request: Request, fieldID: str, sensorID: str):
        return self.sb.addFieldToSensor(sensorID, fieldID)
    
    def addSensor(self, request: Request, sensorID: str):
        return self.sb.createSensor(sensorID)
    
    def getFarmerSensorData(self, request: Request, sensorID: str, fieldID:str):
        return self.sb.getFarmerSensorData(fieldID,sensorID)

    def addFieldFarmerSensor(self, request: Request, fieldID: str, sensorID: str):
        return self.sb.addFieldFarmerSensor(fieldID, sensorID)
    

api_instance = API()
app = api_instance.app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
