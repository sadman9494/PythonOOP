from model.user import  User
from abc import ABC ,abstractmethod

class IUserService(ABC):
    @abstractmethod
    def add_user(user :User):
        pass

    @abstractmethod
    def getUsers():
        pass

    @abstractmethod
    def getUserById(id:int):
        pass

    @abstractmethod 
    def  removeUser(id:int):
        pass