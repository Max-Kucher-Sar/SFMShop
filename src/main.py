from database.connection import get_connection


def create_tables():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Соаздание таблицы users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    balance DECIMAL(10, 2) NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Соаздание таблицы products
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    quantity INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Соаздание таблицы orders
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders(
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    product_id INTEGER REFERENCES products(id),
                    total DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        print(f"Таблицы созданы")

create_tables()