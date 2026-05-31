from .exceptions import NegativePriceError, NegativeQuantityError, InsufficientStockError
from .mixins import LoggableMixin, SerializableMixin, ValidatableMixin
from abc import ABC, abstractmethod
from typing import Optional
from .metaclasses import ModelMeta

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass

class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, price: float) -> float:
        return price - self.amount

class Product(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    def __init__(self, name, price, quantity):
        self.name = name
        self.price=price
        self.quantity=quantity
        self.log(f"Создан товар: {self.name}")

    def calculate_price(self, discount: Optional[DiscountStrategy] = None) -> float | None:
        if not discount:
            return self.price
        return discount.apply(self.price)

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

    def sell(self, amount):
        if self.quantity > amount:
            raise InsufficientStockError(f'Не хватает {self.quantity - amount} товара на складе')
        self.quantity = self.quantity - amount

    def get_total_price(self):
        return self.price * self.quantity


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
