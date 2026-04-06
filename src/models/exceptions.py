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