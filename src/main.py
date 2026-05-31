from models.product import Product
from models.user import User
from models.order import Order
from models.metaclasses import ModelMeta

product = Product("Клавиатура", 12000, 10)
print(product.get_total_price)
print(product.get_total_price)