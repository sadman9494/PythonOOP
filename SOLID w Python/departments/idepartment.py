from abc import ABC, abstractmethod

class Idepartment(ABC):
    @abstractmethod
    def add_department(self , name, capacity):
        pass

    @abstractmethod
    def getAlldepartment(self):
        pass

    @abstractmethod
    def removeDepartment(self ,name):
        pass 
