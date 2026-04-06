import re
from .exceptions import ValidationError
class User:
    def __init__(self, name, email):
        if not re.match(r".+@.+\..+", email):
            raise ValidationError("Неверный формат email")

        self.name = name
        self._email = email

    def set_email(self, email):
        if not re.match(r".+@.+\..+", email):
            raise ValidationError("Неверный формат email")
        self._email = email

    def get_info(self):
        return f"Пользователь: {self.name}, Email: {self._email}"

    def get_email(self):
        return f"Почта пользователя: {self._email}"