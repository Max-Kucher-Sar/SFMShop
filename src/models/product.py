from .exceptions import NegativePriceError, NegativeQuantityError, InsufficientStockError
from .mixins import LoggableMixin, SerializableMixin, ValidatableMixin

class Product(LoggableMixin, SerializableMixin, ValidatableMixin):
    def __init__(self, name, price, quantity):
        self.name = name
        self.price=price
        self.quantity=quantity
        self.log(f"Создан товар: {self.name}")

    def validate(self):
        if self.price < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        if self.quantity <= 0:
            raise NegativeQuantityError("Количество не может быть равным или меньше 0")
        return True

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            price=data['price'],
            quantity=data['quantity']
        )

    @staticmethod
    def calculate_discount(price: int, discount: float):
        return price * (1 - discount / 100)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: int):
        if value < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise NegativeQuantityError("Количество не может быть равным или меньше 0")
        self._quantity = value

    def apply_discount(self):
        if self.price > 3000:
            return True
        return False

    def sell(self, amount):
        if self.quantity > amount:
            raise InsufficientStockError(f'Не хватает {self.quantity - amount} товара на складе')
        self.quantity = self.quantity - amount

    def set_price(self, price):
        if price < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        self.price=price

    def get_total_price(self):
        return self.price * self.quantity

    def disgard_purchase(self, amount):
        self.quantity += amount
        return True

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price

    def __str__(self):
        return f"Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}"

    def __repr__(self):
        return f"Product({self.name!r}, {self.price!r}, {self.quantity!r})"
