from abc import ABC , abstractmethod

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

class IEmployee (ABC):
    @abstractmethod
    def add_emp(self, name, age):
        pass

   # @abstractmethod
   # def getEmpById(self ,name):
   #    pass

    @abstractmethod
    def getAllEmp (self):
        pass


class IStorage (ABC):
    @abstractmethod
    def add(name):
        pass
    @abstractmethod
    def getAll():
        pass
    @abstractmethod
    def remove():
        pass

class deptStorage(IStorage):
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


class deptService(Idepartment):
    
    def  __init__(self, storage : IStorage):
        self.storage = storage
        
    def add_department(self, name, capacity):
        self.storage.add(name, capacity)
    
    def getAlldepartment(self):
        return self.storage.getAll()
    
    def removeDepartment(self,name):
        self.storage.remove(name)
        print (f"{name} is deleted")
        


if __name__ == "__main__":
    department_storage = deptStorage()
    department_service = deptService(department_storage)

    department_service.add_department("HR", 50)
    department_service.add_department("IT", 30)

    print(department_service.getAlldepartment()) 

    department_service.removeDepartment("HR")