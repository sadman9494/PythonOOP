from abc import ABC, abstractmethod

class IEmployee(ABC):
    @abstractmethod
    def add_emp(self, name, age):
        pass

    @abstractmethod
    def rmvEmp(self, name):
        pass

    @abstractmethod
    def getAllEmp(self):
        pass
