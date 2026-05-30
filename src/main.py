from models.product import Product, PercentDiscount, FixedDiscount


product = Product("Ноутбук", 15000, 20)
fixed_disc = FixedDiscount(2000)
percent_disc = PercentDiscount(20)

print("Итоговая цена без скидки", product.calculate_price())
print("Цена с фиксированной скидкой", product.calculate_price(fixed_disc))
print("Цена с 20-ти процентной скидкой", product.calculate_price(percent_disc))

"""Рефакторинг класса PaymentProcessor"""
print("-" * 50)
print("Рефакторинг класса PaymentProcessor")
print("*" * 50)
from models.payment import Payment, CardPayment, PayPalPayment, BankTransferPayment
from service.payment_service import PostgreSQLDatabase, EmailNotification, PaymentProcessor

#БД для хранения
database = PostgreSQLDatabase()

#Используем систему Email для отправки уведомлений
email = EmailNotification()

#Создаем оплату
payment1_method = CardPayment()
payment1 = Payment(1, 15000, payment1_method.payment_method)

payment2_method = BankTransferPayment()
payment2 = Payment(2, 17000, payment2_method.payment_method)


result1 = PaymentProcessor(payment1_method, database, email).process_payment(payment1)
print("Результат выполнения 1-го платежа:", result1)
print("*" * 50)
result2 = PaymentProcessor(payment2_method, database, email).process_payment(payment2)
print("Результат выполнения 2-го платежа:", result2)
