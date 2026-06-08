from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, obj: object):
        pass

class PostgreSQLDatabase(Database):
    def save(self, obj: object):
        print(f"Сохранение экземляра в БД: {obj.__name__}")
