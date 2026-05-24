import functools
import time
from typing import List, Dict

def measure_time(func):
    """Генератор для оценки производительности"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_fin = time.time()
        time_diff = time_fin - time_start
        print(f"Время выполнения функции {func.__name__!r} = {time_diff:.4f} секунд")
        return result
    return wrapper

def log_call(func):
    """Генератор для просмотра имени функции и ее аргументов"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов: {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_call
@measure_time
def calculate_total_orders(orders):
    """Рассчитать общую сумму всех заказов"""
    for order in orders:
        order['total'] = sum(item['price'] * item['quantity'] for item in order['items'])
    return orders

orders = [
    {"name": "Заказ 1", 'items': [{"price": 50000, "quantity": 3}, {"price": 1500, "quantity": 10}]},
    {"name": "Заказ 2", 'items': [{"price": 25000, "quantity": 2}, {"price": 1500, "quantity": 5}]},
    {"name": "Заказ 3", 'items': [{"price": 8000, "quantity": 10}, {"price": 3000, "quantity": 4}]},
]
# total_orders = calculate_total_orders(orders)
# print(total_orders)

products = [
    {"id": 1, "name": "Ноутбук", "price": 50000},
    {"id": 2, "name": "Мышь", "price": 1500},
    {"id": 3, "name": "Монитор", "price": 25000},
    {"id": 4, "name": "Клавиатура", "price": 3000},
    {"id": 5, "name": "Наушники", "price": 8000}
]

def expensive_products(products, min_price) -> Dict:
    for product in products:
        if product['price'] > min_price:
            yield product

for product in expensive_products(products, 5000):
    print(f"Товар с ценой больше 5000: {product['name']}")

# total = sum(product['price'] for product in expensive_products(products, 5000))
# print(f"Итоговая стоимость товаров с ценой больше 5000: {total}")
