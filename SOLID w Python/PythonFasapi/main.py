from fastapi import FastAPI
from typing import Dict
from service.storage import storageService
from service.UserService import userService
from model.user import User

app = FastAPI()

dao = storageService()
user_service = userService(dao)

@app.post("/user/create")
async def create_user(_user :User)->str:
     return user_service.add_user(_user)

@app.get("/user/getAllUsers")
async def getUserInfo()->Dict[int , User]:
    return user_service.getUsers()

@app.get("/user/getUserById/{id}")
async def getUserById(id : int):
     return user_service.getUserById(id)

@app.delete("/user/removeUser/{id}")
async def removeUser(id:int):
     return user_service.removeUser(id)