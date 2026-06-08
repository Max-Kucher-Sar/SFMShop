from .exceptions import NegativePriceError, NegativeQuantityError, InsufficientStockError
from .mixins import LoggableMixin, SerializableMixin, ValidatableMixin
from abc import ABC, abstractmethod
from typing import Optional
from .metaclasses import ModelMeta
from .descriptors import PositiveNumber, CachedProperty
from src.service.database_service import Database
from src.service.discount_service import DiscountStrategy


class Product(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    price = PositiveNumber("_price")
    quantity = PositiveNumber("_quantity")

    def __init__(self, name, price, quantity):
        self.name = name
        self.price=price
        self.quantity=quantity
        self.log(f"Создан товар: {self.name}")

    @CachedProperty
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

class ProductCalculator:

    @staticmethod
    def calculate_price(product: Product, discount: Optional[DiscountStrategy] = None) -> float | None:
        if not discount:
            return product.price
        return discount.apply(product.price)

    @staticmethod
    def sell(product: Product, amount: int):
        if product.quantity < amount:
            raise InsufficientStockError(f'Не хватает {product.quantity - amount} товара на складе')
        product.quantity = product.quantity - amount

class ProductRepo:
    def __init__(self, product: Product):
        self.product = product

    def save_to_database(self, database: Database):
        database.save(self.product)
        return True

product = Product("Ноутбук", 1000, 10)
print(product.get_total_price)  # Вычисление... 10000
print(product.get_total_price)

print(ModelMeta._registry)
print(product.to_dict())