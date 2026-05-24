import time

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

def find_product_in_list(products: list, product_id: int) -> dict | None:
    """Поиск в списке (медленный)"""
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def create_product_dict(products: list) -> dict:
    """Поиск в словаре (медленный)"""
    return {product['id']: product for product in products}

def create_product_list() -> list:
    res = list()
    for i in range(1200):
        info = {
            'id': i,
            'name' : "Ноутбук"
        }
        res.append(info)
    return res

def measure_difference():
    example_id = 989

    products_list = create_product_list()

    # Замеряем время выполнения поиска в списке по example_id
    time_start = time.time()
    find_product_in_list(products_list, example_id)
    time_fin = time.time()
    time_diff_product_list = time_fin - time_start
    print(f"Время выполнения поиска в списке: {time_diff_product_list}")

    #Замеряем время выполнения поиска в словаре по example_id
    products_dict = create_product_dict(products_list)
    time_start = time.time()
    products_dict.get(str(example_id))
    time_fin = time.time()
    time_diff_product_dict = time_fin - time_start
    print(f"Время выполнения поиска в словаре: {time_diff_product_dict}")

    result = time_diff_product_list / time_diff_product_dict
    print(f"Разница во времени между поиском в списке и поиском в словаре = {result}")

measure_difference()


