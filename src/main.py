from models.product import Product
from models.user import User
from models.order import Order
from models.metaclasses import ModelMeta

product = Product("Ноутбук", 15000, 20)
user = User('Bob', 'bob@example.com')
order = Order(1, "2026-05-31", 20, [product])

print(ModelMeta._registry)
print(product.to_dict())
print(user.to_dict())
print(order.to_dict())