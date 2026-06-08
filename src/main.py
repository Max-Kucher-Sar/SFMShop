from models.product import Product, ProductCalculator
from service.discount_service import PercentDiscount, FixedDiscount

product = Product("Клавиатура", 12000, 10)
discount = PercentDiscount(25)

print(product.get_total_price)
print(ProductCalculator.calculate_price(product, discount))
print(ProductCalculator.sell(product, 5))
print(product.quantity)