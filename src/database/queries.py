from .connection import get_connection
import psycopg
from psycopg import IsolationLevel

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
        
def read_user_balance(user_id):
    """
    В данных фукнции используется READ_COMMITTED уровень изоляции.
    По скольку в других транзакциях может изменяться баланс пользователя.
    READ_COMMITTED - позволяет читать данные которые были записаны до начала текущей транзации.
    """
    with get_connection() as conn:
        conn.set_isolation_level(IsolationLevel.READ_COMMITTED)
        with conn.cursor() as cursor:
            res = cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id, ))
            return res.fetchone()
        
def calculate_total_revenue(product_id):
    """
    В данных фукнции используется REPEATABLE READ уровень изоляции.
    REPEATABLE READ позволяет читать данные вне зависимости от того,
    что другие транзакции могут изменять эти строки.
    """
    with get_connection() as conn:
        conn.set_isolation_level(IsolationLevel.REPEATABLE_READ)
        with conn.cursor() as cursor:
            # Количество заказов определенного продукта
            res = cursor.execute("SELECT COUNT(product_id) FROM orders WHERE product_id = %s", (product_id, ))
            count_orders_product = res.fetchone()[0]

            #Общая сумма заказов этого продукта
            res = cursor.execute("SELECT SUM(total) FROM orders WHERE product_id = %s", (product_id, ))
            total_price_ordered_products = res.fetchall()[0][0]

            return {"count": count_orders_product, "price_total" : float(total_price_ordered_products)}
        
def critical_financial_operation(user_from, user_to, amount):
    """
    В данной фукнции реализована критическая финансовая операция.
    Пользователь 1 переводит деньги пользователю 2.
    Нужно изолировать транзакцию от других.
    Уровень изоляции SERIALIZABLE с retry-логикой
    """
    import time
    MAX_RETRIES = 3
    RETRY_DELAY = 0.5
    for attempt in range(MAX_RETRIES + 1): 
        try:
            with get_connection() as conn:
                conn.set_isolation_level(IsolationLevel.SERIALIZABLE)
                with conn.cursor() as cursor:
                    res = cursor.execute("SELECT balance FROM users WHERE id = %s", (user_from, ))
                    balance_user_from = res.fetchone()[0]
                    if balance_user_from < amount:
                        raise ValueError(f"Недостаточно средств у id = {user_from}")
                    
                    res = cursor.execute("SELECT * FROM users WHERE id = %s", (user_to, ))
                    user_to_exist = res.fetchone()
                    if not user_to_exist:
                        raise ValueError(f"Пользователь с id = {user_to} не существует")
                    
                    #Списание денег
                    cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_from))

                    #Начисление
                    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_to))
            print("Перевод успешно совершен!")
            return True
            
        except psycopg.errors.SerializationFailure as e:
            last_error = e
            print(f"Попытка №{attempt}. Ошибка SERIALIZABLE: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"Попытка №{attempt}. Ошибка: {e}")
    print("Все попытки исчерпаны")
    return False

def disgard_cash():
    from psycopg import Connection
    from .connection import DB_CONFIG

    with Connection.connect(**DB_CONFIG) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("DISCARD ALL")
    return True

def measure_index_performance():
    """
    Измерение производительности с индексами и без.
    Из-за малого количество записей Seq Scan быстрее, чем Index Scan.
    Также влияет кэш, второй запрос выполняется быстрее.
    """
    import time
    from random import randint, choice
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Создаем тестовые заказы для пользователя с id = 1
                products_ids = [1, 2, 3, 4, 5]
                for i in range(150):
                    cursor.execute(
                        "INSERT INTO orders (user_id, product_id, total) VALUES (%s, %s, %s)",
                        (1, choice(products_ids), randint(100, 10000))
                    )
                conn.commit()

                # Замер длля запроса без индекса для продукта с id = 2,
                # тк если делать для user_id, то будет возврашать всю таблицу 
                # и не будет наглядности в скорости выполнения
                start = time.perf_counter()
                res = cursor.execute(
                    "SELECT SUM(total) FROM orders WHERE product_id = %s",
                    (2, )
                )
                total_sum_whithout = res.fetchone()[0]
                total_time_whithout = time.perf_counter() - start
                print(f"Время запроса без индекса: {total_time_whithout:.4f}. Результат: {total_sum_whithout}")

                #Сбрасываем кэш
                disgard_cash()

                # Создаем индекс по product_id
                cursor.execute(
                    f"CREATE INDEX IF NOT EXISTS idx_orders_product_id  ON orders (product_id)"
                )
                conn.commit()

                # Замер запроса с индексов
                start = time.perf_counter()
                res = cursor.execute(
                    "SELECT SUM(total) FROM orders WHERE product_id = %s",
                    (2, )
                )
                total_sum = res.fetchone()[0]
                total_time = time.perf_counter() - start
                print(f"Время запроса без индекса: {total_time:.4f}. Результат: {total_sum}")

                # Вычисляем коэффициент ускорения
                speed_rate = total_time_whithout / total_time
                print(f"Ускорение равно = {speed_rate:.4f}")
            return True 
    except Exception as e:
        print(f"Ошибка при замере разницы с индексом/без: {e}")
        return False


