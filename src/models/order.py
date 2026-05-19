from .exceptions import InvalidOrderError, InvalidProductError, NegativeQuantityError
from .product import Product

class Order:
    def __init__(self, user, products, quantity):
        self.user = user

        if not products:
            raise InvalidOrderError("Пустой список товаров")
        self.products = products

        if quantity <= 0:
            raise NegativeQuantityError("Количество не может быть равным или меньше 0")
        self.quantity=quantity


    def add_product(self, product):
        if not isinstance(product, Product):
            raise InvalidProductError("Невалидный тип продукта")
        self.products.append(product)


    def calculate_total(self):
        total_price = 0
        for product in self.products:
            total_price += product.get_total_price()
        return total_price

    def __str__(self):
        total = self.calculate_total()
        return f"Заказ пользователя {self.user.name} на сумму {total} руб."