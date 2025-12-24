from Iservice.IUserService import IUserService
from Iservice.IStorage import IStorage
from model.user import User
from typing import Dict

class userService(IUserService):
    
    def __init__(self, _storage :IStorage):
        self.storage = _storage

    def add_user(self, user: User):
        return self.storage.creat(user)

    def getUserById(self,id: int):
        return self.storage.getById(id)
        

    def getUsers(self):
        return self.storage.getAll()
 
    def removeUser(self,id: int):
        return self.storage.remove(id)
