from .exceptions import InvalidOrderError, InvalidProductError, NegativeQuantityError, NegativeProductsError
from .product import Product
from datetime import datetime
from .mixins import LoggableMixin, SerializableMixin, ValidatableMixin
from typing import Optional
from .metaclasses import ModelMeta
from ..service.database_service import Database
from .descriptors import PositiveNumber
from ..service.discount_service import DiscountStrategy


class Order(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    quantity = PositiveNumber("_quantity")

    def __init__(self, order_id: int, created_at: str, quantity: int, products: list[Product]):
        self.order_id = order_id
        self.quantity=quantity
        self.created_at = datetime.strptime(created_at, "%Y-%m-%d")
        self.products = products
        self.log(f"Создан заказ с id={self.order_id}")

    def __lt__(self, other):
        return self.created_at < other.created_at

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __repr__(self):
        return f"Order(order_id={self.order_id}, created_at={self.created_at}, quantity={self.quantity}, products={self.products})"


class OrderValidate:
    @staticmethod
    def validate(order: Order):
        if not order.products:
            raise NegativeProductsError("Заказ не может быть пустым")
        return True

class OrderCalculate:
    @staticmethod
    def calculate_total(order: Order) -> float:
        return sum(product.get_total_price() for product in order.products)

class OrderRepo:
    def __init__(self, order: Order):
        self.order = order

    def save_to_database(self, database: Database):
        database.save(self.order)
        return True