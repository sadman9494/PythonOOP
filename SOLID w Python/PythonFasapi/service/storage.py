from Iservice.IStorage import IStorage
from model.user import User
from typing import Dict

class storageService(IStorage):
    def __init__(self):
        self.userInfo : Dict[int , User] = {}

    def creat(self,User: User):
        if User.id not in self.userInfo:
            self.userInfo[User.id] = User
            print (self.userInfo)
            return   f"{User.userName} is created"

        else:
            return   f"{User.userName} already exist"
        
    def getAll(self)->Dict[int , User]:
        print (self.userInfo)
        return  self.userInfo
    
    def getById(self, id: int):
        if id in self.userInfo:
            return f" Employee name:{self.userInfo[id].userName} , id:{self.userInfo[id].id}, age: {self.userInfo[id].age}  "

        else:
            return f"{id} does not exist"
        
    def remove(self, id: int):
        if id in self.userInfo:
            del self.userInfo[id]
            return f"{id} is removed"
        else:
            return "This user is not found."
    

        