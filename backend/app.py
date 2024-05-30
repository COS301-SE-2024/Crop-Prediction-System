from backend.model.base import initModel
from fastapi import FastAPI
# from backend.database.supabaseFunctions import signUp, login, logout, getUser
# from backend.database.supabaseFunctions import sbGetFieldInfo

app = FastAPI()

@app.get("/")
def main():
    return initModel()

@app.get("/getFieldInfo")
def getFieldInfo():
    return initModel()

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