from database.connection import get_connection
from database.queries import transfer_money, check_user_balance
import psycopg2

balance_before_res1 = check_user_balance(1)
res1 = transfer_money(1, 3, 1000)
balance_after_res1 = check_user_balance(1)
balance_user3 = check_user_balance(3)
print(f"Результат 1-й попытки: . Количество до: {balance_before_res1}, после: {balance_after_res1}. У пользователя 3: {balance_user3}")

balance_before_res2 = check_user_balance(2)
try:
    res2 = transfer_money(2, 3, 1000)
except Exception as e:
    pass
balance_after_res2 = check_user_balance(2)
balance_user3 = check_user_balance(3)
print(f"Результат 2-й попытки (Должна быть ошибка что не хватает средств). Количество до: {balance_before_res2}, после: {balance_after_res2}. У пользователя 3: {balance_user3}")
