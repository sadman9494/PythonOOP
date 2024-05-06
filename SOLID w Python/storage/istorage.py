from abc import ABC, abstractmethod
from typing import List

class IStorage(ABC):
    @abstractmethod
    def add(self, name: str, capacity: int) -> None:
        pass
    
    @abstractmethod
    def getAll(self) -> List[str]:
        pass
    
    @abstractmethod
    def remove(self, name: str) -> None:
        pass
