from .connection import get_connection
import psycopg

def create_order(user_id, product_id, quantity, total):
    """Создание заказа с атомарными операциями"""
    
    with get_connection() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO orders (user_id, product_id, total) VALUES (%s, %s, %s)""", 
                    (user_id, product_id, total)) 

                cursor.execute(
                    "UPDATE products SET quantity = quantity - %s WHERE id = %s",
                    (quantity, product_id)
                )

                total_quantity_stmt = cursor.execute(
                    "SELECT quantity FROM products WHERE id = %s",
                    (product_id, )
                )
                total_quantity = total_quantity_stmt.fetchone()
                if total_quantity[0] < quantity:
                    raise ValueError("Недостаточно товара")
                
            return "Заказ создан"
        except psycopg.Error as e:
            # Ошибка БД - rollback выполняется автоматически
            conn.rollback()
            print(f"Ошибка БД: {e}")
            raise
        except Exception as e:
            conn.rollback()
            print(f"Ошибка логики: {e}")
            raise

def get_quantity_of_products(product_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            res = cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id, ))
            return res.fetchone()
        
def transfer_money(from_user_id, to_user_id, amount):
    """Перевод денег от одного пользователя другому"""
    with get_connection() as conn:
        try:
            with conn.cursor() as cursor:
                #Проверяем достаточно ли денег на балансе пользователя с которого списываем
                has_user_balance_stmt = cursor.execute(
                    "SELECT balance FROM users WHERE id = %s",
                    (from_user_id, )
                )
                has_user_balance = has_user_balance_stmt.fetchone()
                if has_user_balance[0] < amount:
                    raise ValueError("Недостаточно средств")
                
                #Переводим средства
                cursor.execute(
                    "UPDATE users SET balance = balance + %s WHERE id = %s",
                    (amount, to_user_id)
                )
                #Списываем средства
                cursor.execute(
                    "UPDATE users SET balance = balance - %s WHERE id = %s",
                    (amount, from_user_id)
                )
            return True
        except psycopg.Error as e:
            # Ошибка БД - rollback выполняется автоматически
            conn.rollback()
            print(f"Ошибка БД: {e}")
            raise
        except Exception as e:
            conn.rollback()
            print(f"Ошибка логики: {e}")
            raise

def check_user_balance(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            res = cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id, ))
            return res.fetchone()