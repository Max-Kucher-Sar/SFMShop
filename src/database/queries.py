from src.models.exceptions import (
InsertError, UpdateError, SelectError, DeleteError
)

def create_order_items(conn, order_id, product_id, quantity, price):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, product_id, quantity, price)
                )
        return True
    except Exception as e:
        raise InsertError(f'Ошибка добавления записи в таблицу order_items: {e}')

def get_orders_with_products(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT orders.id as order_id,
                products.name as product_name,
                order_items.quantity as quantity,
                order_items.price as price
                FROM orders
                INNER JOIN order_items ON order_items.order_id = orders.id
                INNER JOIN products ON products.id = order_items.product_id
                WHERE orders.user_id = %s
                """, (user_id, )
            )
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise SelectError(f"Ошибка получения записи из таблицы orders по user_id = {user_id}: {e}")

def get_user_order_history(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                orders.id,
                products.name as product_name,
                order_items.quantity as quantity
                FROM users
                INNER JOIN orders ON orders.user_id = users.id
                INNER JOIN order_items ON order_items.order_id = orders.id
                INNER JOIN products ON products.id = order_items.product_id
                WHERE orders.user_id = %s
                ORDER BY orders.created_at DESC
                """,
                (user_id,)
            )
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise SelectError(f"Ошибка получения записи из таблицы users по user_id = {user_id}: {e}")

def get_order_statistics(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                user_id,
                users.name,
                COUNT(*) as order_count,
                SUM(total)
                FROM orders
                INNER JOIN users on users.id = orders.user_id
                GROUP BY user_id, users.name
                ORDER BY user_id ASC
                """
            )
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise SelectError(f"Ошибка получения записей из таблицы orders: {e}")

def get_top_products(conn, limit=5):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                name,
                products.price,
                SUM(order_items.quantity) as total_quantity
                FROM products
                INNER JOIN order_items on order_items.product_id = products.id
                GROUP BY products.id
                ORDER BY total_quantity DESC 
                LIMIT %s
                """, (limit, )
            )
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise SelectError(f"Ошибка получения записей из таблицы products: {e}")
