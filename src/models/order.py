from .exceptions import InvalidOrderError, InvalidProductError, NegativeQuantityError, NegativeProductsError
from .product import Product
from datetime import datetime
from .mixins import LoggableMixin, SerializableMixin, ValidatableMixin
from typing import Optional
from .metaclasses import ModelMeta

class Order(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    def __init__(self, order_id: int, created_at: str, quantity: int, products: list[Product]):
        self.order_id = order_id
        self.quantity=quantity
        self.created_at = datetime.strptime(created_at, "%Y-%m-%d")
        self.products = products
        self.log(f"Создан заказ с id={self.order_id}")


    def add_product(self, product):
        if not isinstance(product, Product):
            raise InvalidProductError("Невалидный тип продукта")
        self.products.append(product)


    def __lt__(self, other):
        return self.created_at < other.created_at

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __repr__(self):
        return f"Order(order_id={self.order_id}, created_at={self.created_at}, quantity={self.quantity}, products={self.products})"


class OrderValidate:
    @staticmethod
    def validate(order: Order):
        if order.quantity <= 0:
            raise NegativeQuantityError("Количество не может быть равным или меньше 0")
        if not order.products:
            raise NegativeProductsError("Заказ не может быть пустым")
        return True

class OrderCalculate:
    @staticmethod
    def calculate_total(order: Order):
        return sum(product.get_total_price() for product in order.products)