def calculate_order_total(price, discount_rate):
    try:
        result = price * (1 - discount_rate)
        return round(result, 2)
    except TypeError:
        print(
            f'Неверный формат переданных данных:',
            f'price - {type(price)},',
            f'discount_rate - {type(discount_rate)}.',
            f'Ожидает - (int, float)'
        )

def get_discount_by_total(total):
    """
    Функция возвращает размер скидки исходя из цены заказа
    """
    try:
        if total <= 0:
            return 0
        elif total > 10000:
            return 0.15
        elif total > 5000:
            return 0.1
        else:
            return 0.05
    except TypeError:
        print(
            f'Неверный формат переданных данных:',
            f'total - {type(total)},',
            f'ожидает - (int, float)'
        )

