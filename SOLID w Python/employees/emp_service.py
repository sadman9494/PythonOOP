from employees.iemployee import IEmployee
from storage.istorage import IStorage

class EmpService(IEmployee):
    def __init__(self, storage: IStorage):
        self.storage = storage

    def add_emp(self, name, age):
        self.storage.add(name, age)

    def getAllEmp(self):
        return self.storage.getAll()

    def rmvEmp(self, name):
        self.storage.remove(name)
