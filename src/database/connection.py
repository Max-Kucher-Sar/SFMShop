import os
import psycopg2
from dotenv import load_dotenv
from src.models.exceptions import (
InsertError, UpdateError, SelectError
)

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="postgres",
    user="postgres",
    password=os.getenv("pswd", "password")
    )

def connect_to_db():
    return conn

def add_product(conn, name, price, quantity):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
                (name, price, quantity)
            )
    return True

def get_all_products(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM products"
        )
        return cursor.fetchall()

def update_product_price(conn, product_id, new_price):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE products SET price = %s WHERE id = %s",
                    (new_price, product_id)
                )
                return True
    except Exception as e:
        raise UpdateError(f"Ошибка обновления записи из products products по id = {product_id}: {e}")

def create_user(conn, name, email):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    (name, email)
                )
        return True
    except Exception as e:
        raise InsertError(f'Ошибка добавления записи в таблицу users: {e}')

def get_user_by_id(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id, )
            )
            return cursor.fetchone()
    except Exception as e:
        raise SelectError(f"Ошибка получения записи из таблицы users по id = {user_id}: {e}")

def create_order(conn, user_id, total):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO orders (user_id, total) VALUES (%s, %s)",
                    (user_id, total)
                )
        return True
    except Exception as e:
        raise InsertError(f'Ошибка добавления записи в таблицу orders: {e}')

def get_user_orders(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM orders WHERE user_id = %s",
                (user_id, )
            )
            return cursor.fetchone()
    except Exception as e:
        raise SelectError(f"Ошибка получения записи из таблицы users по id = {user_id}: {e}")

def create_order_item(conn, order_id, product_id, quantity, price):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s)",
                    (order_id, product_id, quantity, price)
                )
        return True
    except Exception as e:
        raise InsertError(f'Ошибка добавления записи в таблицу users: {e}')