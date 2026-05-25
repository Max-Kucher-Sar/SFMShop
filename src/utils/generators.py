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

def calculate_fast_total_orders(orders):
    """Рассчитать общую сумму всех заказов"""
    return sum(
        item['price'] * item['quantity']
        for order in orders
        for item in order['items']
    )

def calculate_slow_total_orders(orders):
    total = 0
    for order in orders:
        for item in order['items']:
            total += item['price'] * item['quantity']
    return total

orders = [
    {"name": "Заказ 1", 'items': [{"price": 50000, "quantity": 3}, {"price": 1500, "quantity": 10}]},
    {"name": "Заказ 2", 'items': [{"price": 25000, "quantity": 2}, {"price": 1500, "quantity": 5}]},
    {"name": "Заказ 3", 'items': [{"price": 8000, "quantity": 10}, {"price": 3000, "quantity": 4}]},
]

def measuring_extra_cycles():
    # Замеряем время выполнения поиска суммы по вложенным циклам
    time_start = time.time()
    calculate_slow_total_orders(orders)
    time_fin = time.time()
    time_diff_slow_sum = time_fin - time_start
    print(f"Время расчета итоговой суммы по вложенным циклам: {time_diff_slow_sum}")

    # Замеряем время расчета суммы по встроенной функции
    time_start = time.time()
    calculate_fast_total_orders(orders)
    time_fin = time.time()
    time_diff_fast_sum = time_fin - time_start
    print(f"Время расчета итоговой суммы по встроенной функции: {time_diff_fast_sum}")

    result = time_diff_slow_sum / time_diff_fast_sum
    print(f"Разница во времени между расчетами по циклам и встроенной функции = {result}")

products = [
    {"id": 1, "name": "Ноутбук", "price": 50000},
    {"id": 2, "name": "Мышь", "price": 1500},
    {"id": 3, "name": "Монитор", "price": 25000},
    {"id": 4, "name": "Клавиатура", "price": 3000},
    {"id": 5, "name": "Наушники", "price": 8000}
]

def expensive_products(products, min_price):
    for product in products:
        if product['price'] > min_price:
            yield product

# for product in expensive_products(products, 5000):
#     print(f"Товар с ценой больше 5000: {product['name']}")

# total = sum(product['price'] for product in expensive_products(products, 5000))
# print(f"Итоговая стоимость товаров с ценой больше 5000: {total}")
