from departments.idepartment import Idepartment
from storage.istorage import IStorage

class DeptService(Idepartment):
    def __init__(self, storage: IStorage):
        self.storage = storage
        
    def add_department(self, name, capacity):
        self.storage.add(name, capacity)
    
    def getAlldepartment(self):
        return self.storage.getAll()

    def removeDepartment(self, name):
        self.storage.remove(name)
