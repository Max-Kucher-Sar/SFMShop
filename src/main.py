from models.product import Product
from models.order import Order
from models.user import User
from models.payment import CardPayment, PayPalPayment
from models.exceptions import (
NegativePriceError, InsufficientStockError,
ValidationError, InvalidOrderError, NegativeQuantityError, InvalidProductError
)

from database.connection import (
connect_to_db, add_product, get_all_products, update_product_price,
create_user, get_user_by_id, create_order, get_user_orders, delete_order
)

from database.queries import (
create_order_items, get_orders_with_products, get_user_order_history,
get_order_statistics, get_top_products
)


# conn = connect_to_db()
# try:
#     new_username = 'Саша'
#     new_user_email = 'sasha@mail.ru'
#     create_user(conn, new_username, new_user_email)
#     print(f"Новый пользователь с именем {new_username!r} и почтой {new_user_email!r} создан!")
#
#     products = get_all_products(conn)
#     print("Все товары:", products)
#
#     orders_stat = get_order_statistics(conn)
#     print('Статистика по заказам:', orders_stat)
#
#     top_prod = get_top_products(conn, limit=5)
#     print('Топ товаров:', top_prod)
#
#     res_user = get_user_by_id(conn, 1)
#     print('Пользователь:', res_user)
#
#     user_id = 2
#     user = get_user_order_history(conn, user_id)
#     print(f'Заказ пользователя с id {user_id!r}:', user)
# finally:
#     conn.close()

from random import randint
from datetime import datetime, timedelta
import time

def create_orders_list():
    current_date = datetime(2026, 5, 1)
    orders = list()
    for i in range(2, 31):
        info = {
            "price": randint(0, 5000),
            "created_at": current_date + timedelta(days=randint(2, 100))
        }
        orders.append(info)
    return orders

def bubble_sort(orders_list):
    n = len(orders_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if orders_list[j]['created_at'] > orders_list[j+1]['created_at']:
                orders_list[j], orders_list[j+1] = orders_list[j+1], orders_list[j]

def measure_difference():
    orders_list = create_orders_list()

    # Замеряем время выполнения ручной (пузырьковой) сортировки
    time_start = time.time()
    bubble_sort(orders_list)
    time_fin = time.time()
    time_diff_bubble_sort = time_fin - time_start
    print(f"Время ручной сортировки: {time_diff_bubble_sort}")

    # Замеряем время выполнения сортировки через sorted()
    time_start = time.time()
    sorted(orders_list, key=lambda x: x['created_at'])
    time_fin = time.time()
    time_diff_sorted_method = time_fin - time_start
    print(f"Время выполнения сортировки через sorted(): {time_diff_sorted_method}")

    result = time_diff_bubble_sort / time_diff_sorted_method
    print(f"В {round(result, 2)} раз метод sorted() быстрее ручной сортировки")
    """
    В то время как пузырьковая сортировка обладает квадратичной сложностью (использовались вложенные циклы),
    sorted() быстрее, потому что обладает линейной сложностью.
    И чаще всего, встроенные методы в python работают быстрее, чем руками написанный код
    """

measure_difference()