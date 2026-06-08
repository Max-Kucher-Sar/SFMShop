from models.order_factory import OrderFactory
from models.delivery_strategy import StandardDelivery
from models.payment import CardPayment
from models.product import Product


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

process_advanced_order_system()