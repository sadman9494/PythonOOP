from pydantic import BaseModel
from typing import List

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