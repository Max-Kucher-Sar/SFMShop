from models.product import Product
from models.order import Order
from models.user import User
from models.payment import CardPayment, PayPalPayment
from models.exceptions import (
NegativePriceError, InsufficientStockError,
ValidationError, InvalidOrderError, NegativeQuantityError, InvalidProductError
)

def process_order_system():
    user = User("Иван", "ivan@test.com")

    #Тестируем исключение при валидации email
    try:
        user.set_email("ivan_test.com")
    except ValidationError as e:
        print(f"Ошибка при обновлении email пользователя: {e}")

    print(user.get_email())

    product1 = Product("Ноутбук", 50000, 2)
    product2 = Product("Мышь", 1500, 3)

    order = Order(user, [product1, product2])
    # Тестируем исключение при добавлении невалидного продукта
    try:
        order.add_product("Клавиатура")
    except InvalidProductError as e:
        print(f"Ошибка при добавлении товара в заказ: {e}")

    total = order.calculate_total()
    print("Общая стоимость заказа:", total)

    payments = [
        CardPayment(1000, "1234 5678 9012 3456"),
        PayPalPayment(2000, "test@paypal.com")
    ]

    for payment in payments:
        print(payment.process_payment())

    sorted_products = sorted([product1, product2])
    for product in sorted_products:
        print(product)

    try:
        product.set_price(-1000)
    except NegativePriceError as e:
        print("Ошибка валидации:", e)

process_order_system()