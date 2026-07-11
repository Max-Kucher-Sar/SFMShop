from database.connection import get_connection
from database.queries import calculate_total_revenue, read_user_balance, critical_financial_operation
import psycopg2

res = critical_financial_operation(3, 2, 500)
print(res)