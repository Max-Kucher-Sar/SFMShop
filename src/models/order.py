from .exceptions import InvalidOrderError, InvalidProductError, NegativeQuantityError
from .product import Product
from datetime import datetime

class Order:
    def __init__(self, order_id: int, created_at: str, quantity: int):
        self.order_id = order_id
        # self.user = user

        # if not products:
        #     raise InvalidOrderError("Пустой список товаров")
        # self.products = products

        if quantity <= 0:
            raise NegativeQuantityError("Количество не может быть равным или меньше 0")
        self.quantity=quantity

        self.created_at = datetime.strptime(created_at, "%Y-%m-%d")

    def add_product(self, product):
        if not isinstance(product, Product):
            raise InvalidProductError("Невалидный тип продукта")
        self.products.append(product)


    def calculate_total(self):
        total_price = 0
        for product in self.products:
            total_price += product.get_total_price()
        return total_price

    def __lt__(self, other):
        return self.created_at < other.created_at

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __str__(self):
        total = self.calculate_total()
        return f"Заказ пользователя {self.user.name} на сумму {total} руб."

    def __repr__(self):
        return f"Order(order_id={self.order_id}, created_at={self.created_at}, quantity={self.quantity})"