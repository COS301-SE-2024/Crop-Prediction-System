from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!", "timestamp": datetime.datetime.now().isoformat()}