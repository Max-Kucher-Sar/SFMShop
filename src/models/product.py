from .exceptions import NegativePriceError, NegativeQuantityError, InsufficientStockError

class Product:
    def __init__(self, name, price, quantity):
        self.name = name

        if price < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        self.price=price

        if quantity <= 0:
            raise NegativeQuantityError("Количество не может быть равным или меньше 0")
        self.quantity = quantity

    def check_stock(self) -> int:
        return self.quantity

    def update_stock(self, amount) -> int:
        self.quantity += amount
        return self.quantity

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
