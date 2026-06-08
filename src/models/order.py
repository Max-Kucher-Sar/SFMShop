from src.service.database_service import Database
from .metaclasses import ModelMeta

class Order(metaclass=ModelMeta):

    def __init__(self, order_id, items, user):
        self.order_id = order_id
        self.items = items
        self.user = user

    def __lt__(self, other):
        return self.order_id < other.order_id

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __add__(self, other):
        new_items = self.items + other.items
        return Order(self.order_id, new_items, self.user)

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)


class OrderValidate:
    @staticmethod
    def validate(order: Order):
        if not order.items:
            raise ValueError("Заказ не может быть пустым")
        return True

class OrderCalculate:
    @staticmethod
    def calculate_total(order: Order) -> float:
        return sum(product.get_total_price() for product in order.items)

class OrderRepo:
    def __init__(self, order: Order):
        self.order = order

    def save_to_database(self, database: Database):
        database.save(self.order)
        return True

# Использование
order1 = Order(1, ["Ноутбук", "Мышь"], "Bob")
order2 = Order(2, ["Клавиатура"], "Max")

print(len(order1))  # 2
print("Ноутбук" in order1)  # True
order3 = order1 + order2  # Объединение заказов
sorted_orders = sorted([order2, order1])
print(len(order3))  # 3