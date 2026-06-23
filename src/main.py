import sys
import os

# Добавляем корневую директорию проекта в sys.path для возможности запуска
# как python src/main.py, так и python -m src.main из корня проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.order_factory import OrderFactory
from src.models.delivery_strategy import StandardDelivery
from src.models.payment import CardPayment
from src.models.product import Product


def process_advanced_order_system():
    """Демонстрация всех продвинутых концепций ООП"""

    # 1. Factory для создания заказов
    order = OrderFactory.create_order(1, ["Ноутбук", "Мышь"], "Bob")

    # 2. Strategy для расчета доставки
    delivery = StandardDelivery()
    delivery_cost = delivery.calculate_cost(5.0)

    # 3. Полиморфизм для платежей
    payment = CardPayment()
    payment.process_fee(1000)

    # 4. Метакласс для сериализации
    order_json = order.to_dict()

    # 5. Дескрипторы для валидации
    product = Product("Ноутбук", 1000, 10)  # Автоматическая валидация

    # 6. Миксины для логирования
    payment.log("Платеж обработан")

    # 7. Магические методы
    print(len(order))  # Количество товаров
    print("Ноутбук" in order)  # Проверка наличия

    return {
        "order": order_json,
        "delivery_cost": delivery_cost,
        "product": product.to_dict()
    }

# process_advanced_order_system()
from functools import reduce

product_names = ["Ноутбук", "Мышь"]
product_prices_dict = dict(
    reduce(
        lambda acc, item: acc + [(item[0], item[1])],
        zip(product_names, [1000, 200]),
        []
    )
)
print(product_prices_dict)
