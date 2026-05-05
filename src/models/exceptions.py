class SFMShopException(Exception):
    """Базовое исключение для проекта SFMShop"""
    pass

class ValidationError(SFMShopException):
    """Ошибка валидации данных"""
    pass

class BusinessLogicError(SFMShopException):
    """Ошибка бизнес-логики"""
    pass

class DatabaseError(SFMShopException):
    """Ошибка работы с БД"""
    pass

class NegativePriceError(ValidationError):
    """Отрицательная цена"""
    pass

class NegativeQuantityError(ValidationError):
    """Неверное количество"""
    pass

class InsufficientStockError(BusinessLogicError):
    """Товара недостаточно на складе"""
    pass

class InvalidOrderError(BusinessLogicError):
    """Заказ невалиден"""
    pass

class InvalidProductError(BusinessLogicError):
    """Товар невалиден"""
    pass

class InsertError(DatabaseError):
    """Ошибка добавления записи в БД"""
    pass

class UpdateError(DatabaseError):
    """Ошибка изменения записи в БД"""
    pass

class SelectError(DatabaseError):
    """Ошибка запросов на получение в БД"""
    pass

class DeleteError(DatabaseError):
    """Ошибка запросов на удаление в БД"""
    pass