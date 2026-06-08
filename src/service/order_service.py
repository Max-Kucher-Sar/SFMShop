# Файл src/main.py
def process_order(order_data):
    """Обработка заказа - делает слишком много"""
    # Валидация
    validate_order_data(order_data)

    # Расчет стоимости
    total = calculate_order_total(order_data)

    # Применение скидки
    final_total = calculate_discount(total)

    # Проверка баланса пользователя
    user_balance = check_user_balance(order_data["user_id"], final_total)

    # Сохранение заказа
    order_id = create_order(order_data["user_id"], order_data["items"], final_total)

    # Отправка уведомления
    user_email = get_user_email(order_data["user_id"])
    notify_user(user_email, f"Заказ #{order_id} оформлен на сумму {final_total}")

    # Логирование
    msg = f"Заказ {order_id} обработан: пользователь {order_data['user_id']}, сумма {final_total}"
    log(msg)

    return {
        "order_id": order_id,
        "total": final_total,
        "discount": total - final_total
    }

def validate_order_data(order_data: dict):
    """Функция для валидации заказов"""
    if not order_data.get("user_id"):
        raise ValueError("Нет user_id")
    if not order_data.get("items"):
        raise ValueError("Нет товаров")
    if len(order_data.get("items", [])) == 0:
        raise ValueError("Список товаров пуст")

    for item in order_data["items"]:
        if not item.get("price"):
            raise ValueError("Нет цены товара")
        if not item.get("quantity"):
            raise ValueError("Нет количества")
        if item["price"] < 0:
            raise ValueError("Цена не может быть отрицательной")
        if item["quantity"] <= 0:
            raise ValueError("Количество должно быть положительным")

def calculate_order_total(order_data: dict):
    """Расчет стоимости"""
    return sum(
        item["price"] * item["quantity"]
        for item in order_data["items"]
    )

def calculate_discount(total: int) -> float:
    """Расчет скидки"""
    discount = 0
    if total > 10000:
        discount = 0.15
    elif total > 5000:
        discount = 0.10
    elif total > 1000:
        discount = 0.05
    return total * (1 - discount)

def check_user_balance(user_id: int, final_total: float) -> bool:
    """Проверка баланса пользователя"""
    user_balance = 12000
    if user_balance < final_total:
        raise ValueError("Недостаточно средств")
    return True

def create_order(user_id: int, items: list, final_total):
    """Создание заказа"""
    print(f"Заказ пользователя с id={user_id} создан!")
    print(f"Корзина: {items}")
    print(f"Итоговая цена: {final_total} руб.")

def get_user_email(user_id: int) -> str:
    """Получение почты по id пользователя"""
    return f"example_{user_id}@example.com"

def notify_user(user_email: str, msg: str):
    """Отправка письма"""
    print(f"Пользователю {user_email!r} отправлено письмо: {msg!r}")

def log(msg: str):
    """Логгирование"""
    print(msg)