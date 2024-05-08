from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

class Project(BaseModel):
    projectId: int 
    projectName: str
    stack: List[str] = None

class User(BaseModel):
    id: int 
    userName: str
    age: int = None
    dept: str = None
    stack: List[Project] = None

app = FastAPI()

users_db: List[User] = []

@app.post("/user/create/", response_model=User)
async def create_user(user: User):
    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def get_users():
    return users_db
