from database.connection import get_connection
from database.queries import calculate_total_revenue, read_user_balance, critical_financial_operation, measure_index_performance
import psycopg2

res = measure_index_performance()
print(res)