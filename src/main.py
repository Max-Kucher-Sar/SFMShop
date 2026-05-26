from models.product import Product

product1 = Product('Ноутбук', 15000, 10)

product_info = {
    'name': 'Клавиатура',
    'price': 1500,
    'quantity': 18
}
product2 = Product.from_dict(product_info)

print('Объект с классическим инициализатором:', product1)
print('Объект, созданный через декоратор classmethod:', product2)

total_discount1 = product1.calculate_discount(product1.price, 20)
total_discount2 = Product.calculate_discount(10000, 50)

print("Итоговая сумма с учетом скидки полученная от экземпляра:", total_discount1)
print("Итоговая сумма с учетом скидки полученная от класса:", total_discount2)
