from abc import ABC, abstractmethod

class TableObject(ABC):
    @classmethod
    @abstractmethod
    def from_row(cls, row):
        pass

    @abstractmethod
    def to_row(self):
        pass