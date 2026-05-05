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
create_user, get_user_by_id, create_order, get_user_orders
)

from database.queries import (
create_order_items, get_orders_with_products, get_user_order_history,
get_order_statistics, get_top_products
)


conn = connect_to_db()
try:
    user_1 = get_user_order_history(conn, 1)
    orders_res = get_order_statistics(conn)
    top_orders = get_top_products(conn, limit=3)
    print('Заказ пользователя 1', user_1)
    print('Статистика по пользователям:', orders_res)
    print('Топ товаров:', top_orders)
finally:
    conn.close()

