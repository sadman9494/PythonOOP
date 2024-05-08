from abc import ABC, abstractmethod
from model.user import User
from typing import Dict

class IStorage(ABC):
    
    @abstractmethod
    def creat(User : User):
        pass

    @abstractmethod
    def getAll()->Dict[int , User]:
        pass

    @abstractmethod
    def getById(id : int):
        pass

    @abstractmethod
    def remove (id :int):
        pass
