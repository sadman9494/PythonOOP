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

    @abstractmethod
    def rmvEmp(self ,name):
       pass

    @abstractmethod
    def getAllEmp (self):
        pass


class IStorage (ABC):
    @abstractmethod
    def add(name , value):
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


class empStorage(IStorage):
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

class empService (IEmployee):
    
    def __init__(self, storage : IStorage):
        self.storage = storage

    
    def add_emp(self, name, age):
        self.storage.add(name,age)

    def getAllEmp(self):
        return self.storage.getAll()

    def rmvEmp(self, name):
        self.storage.remove(name)
        


if __name__ == "__main__":
    department_storage = deptStorage()
    department_service = deptService(department_storage)

    employee_storage = empStorage()
    employee_service = empService(employee_storage)

    department_service.add_department("HR", 50)
    department_service.add_department("IT", 30)

    employee_service.add_emp("sakib" , 23)
    employee_service.add_emp("Rahim", 18)
    employee_service.add_emp("sadman" , 23)


    print(department_service.getAlldepartment()) 
    print (employee_service.getAllEmp())

    department_service.removeDepartment("HR")
    employee_service.rmvEmp("Rahim")

    print(department_service.getAlldepartment()) 
    print (employee_service.getAllEmp())