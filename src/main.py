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


conn = connect_to_db()
try:
    new_username = 'Саша'
    new_user_email = 'sasha@mail.ru'
    create_user(conn, new_username, new_user_email)
    print(f"Новый пользователь с именем {new_username!r} и почтой {new_user_email!r} создан!")

    products = get_all_products(conn)
    print("Все товары:", products)

    orders_stat = get_order_statistics(conn)
    print('Статистика по заказам:', orders_stat)

    top_prod = get_top_products(conn, limit=5)
    print('Топ товаров:', top_prod)

    res_user = get_user_by_id(conn, 1)
    print('Пользователь:', res_user)

    user_id = 2
    user = get_user_order_history(conn, user_id)
    print(f'Заказ пользователя с id {user_id!r}:', user)
finally:
    conn.close()

