from .mixins import LoggableMixin, SerializableMixin
from .descriptors import PositiveNumber

class User(LoggableMixin, SerializableMixin):
    balance = PositiveNumber("_balance")

    def __init__(self, user_id, name, email, age, balance):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.balance = balance
        self.orders = []
        self.is_active = True
        self.log(f"Создан пользователь: {self.name}")

