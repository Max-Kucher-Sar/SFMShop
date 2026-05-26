from models.order import Order
from models.cart import ShoppingCart

order1 = Order(1, "2024-01-15", 5000)
order2 = Order(2, "2024-01-16", 3000)
order3 = Order(3, "2024-01-17", 4000)

# Теперь можно сравнивать
# print(order1 < order2) # True
# print(order1 == order2) # False

# Можно сортировать
orders = [order1, order2, order3]
sorted_orders = sorted(orders, reverse=True)
# print(sorted_orders)

user_cart = ShoppingCart()
print("Корзина пользователя до добавления товаров:", user_cart.items)
user_cart = user_cart + "Ноутбук"
user_cart = user_cart + "Клавиатура"
print("Корзина пользователя после добавления товаров:", user_cart.items)
print("Количество товаров в коризне пользователя:", len(user_cart))
for item in user_cart:
    print("Товар:", item)

