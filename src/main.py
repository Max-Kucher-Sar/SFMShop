from models.product import Product
from models.order import Order


product = Product("Ноутбук", 15000, 20)
print(product.is_valid())
print(product.to_json())

print('-' * 50)
print("Тестируем воздействие миксинов на класс Order")
print('-' * 50)

order = Order(1, "2026-05-27", 5)
print(order.is_valid())
print(order.to_json())