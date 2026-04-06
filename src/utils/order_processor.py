from .calculations import calculate_order_total, get_discount_by_total

def load_orders_from_file(filename):
    """
    Выгружает данные о заказах из файла
    """
    try:
        result = list()
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                convert_space = line.strip()
                convert_line = convert_space.split(":")
                result.append(convert_line)
        return result
    except FileNotFoundError:
        print(f'Не найден файл {filename} в папке data')


def process_orders(orders_data):
    """
    Создает список словарей с обработанными заказами
    """
    try:
        result = list()
        for order in orders_data:
            discount = get_discount_by_total(int(order[1]))
            total = calculate_order_total(int(order[1]), discount)
            order_data = {
                "order_id": order[0],
                "total": total,
                "status": order[2],
                "user": order[3]
            }
            result.append(order_data)
        return result
    except ValueError:
        print(f"Ошибка при сборе заказов: неверный тип данных для итоговой сумма заказа")

def analyze_orders(processed_orders):
    """
    Создает словарь со статистикой по заказам
    """
    try:
        stats = {
            "total_orders": 0,
            "total_sum": 0,
            "by_status": {},
            "unique_users": set()
        }
        for order in processed_orders:
            stats["total_orders"] += 1
            stats["total_sum"] += order["total"]
            if order["status"] not in stats["by_status"]:
                stats["by_status"][order["status"]] = 1
            else:
                stats["by_status"][order["status"]] += 1
            stats["unique_users"].add(order['user'])
        stats["unique_users"] = list(stats["unique_users"])
        return stats
    except Exception as e:
        print(f"Ошибка при сборе статистики: {e}")

def process_order_file(input_file, output_file):
    """
    Добавление заказов в файл
    """
    try:
        order_data = load_orders_from_file(input_file)
        if not order_data:
            return f"Произошла ошибка при выводе данных с файла: пустой файл или неверное название файла"

        orders = process_orders(order_data)
        if not orders:
            return f"Произошла ошибка при сборе обработанных заказов"

        stats = analyze_orders(orders)
        if not stats:
            return f"Произошла ошибка при создании статистики"

        orders_status = list()
        for key, value in stats['by_status'].items():
            orders_status.append(f"{key}: {value}")
        res_status = ", ".join(orders_status)

        with open(output_file, 'a') as file:
            lines = [
                f"Обработано заказов: {stats['total_orders']}\n",
                f"Общая сумма: {stats['total_sum']} руб.\n",
                f"По статусам: {res_status}\n",
                f"Уникальных пользователей: {len(stats['unique_users'])}\n"
            ]
            file.writelines(lines)
        return True
    except Exception as e:
        print(f"Произошла ошибка при добавлении заказов в файл: {e}")
