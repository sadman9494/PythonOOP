from storage.istorage import IStorage

class EmpStorage(IStorage):
    def __init__(self):
        self.employees = {}

    def add(self,name,age):
        if name not in self.employees:
             self.employees[name] = age
        else:
            raise Exception('Employee is already exist')
   
    def getAll(self):
        return list(self.employees)
    
    def remove(self , name):
        if name not in self.employees:
            raise Exception('Employee does not exist')
        else:
            self.employees.pop(name)
            print (f"employee name:{name} is removed")
