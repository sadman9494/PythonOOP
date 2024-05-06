from storage.istorage import IStorage

class DeptStorage(IStorage):
    def __init__(self):
        self.departments = {}

    def add(self,name :str , capacity:int):
       if name not in self.departments:
           self.departments[name] = capacity
       else:
           raise Exception("Department already exists") 

    def getAll(self):
        return list(self.departments)
    
    def remove(self, name):
        self.departments.pop(name)
