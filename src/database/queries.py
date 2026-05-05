
def create_order_items(conn, order_id, product_id, quantity, price):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, product_id, quantity, price)
            )
    return True

def get_orders_with_products(conn, user_id):
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

def get_user_order_history(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
            orders.id,
            users.name as username,
            products.name as product_name,
            order_items.quantity as quantity,
            order_items.price as price
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

def get_order_statistics(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT
            user_id,
            COUNT(*) as order_count,
            SUM(total)
            FROM orders
            GROUP BY user_id
            ORDER BY user_id ASC
            """
        )
        result = cursor.fetchall()
    return result

def get_top_products(conn, limit=5):
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