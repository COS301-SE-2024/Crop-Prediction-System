from backend.model.base import initModel
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return initModel()

@app.get("/getFieldInfo")
def getFieldInfo():
    return initModel()
