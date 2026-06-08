class PositiveNumber:
    """Дескриптор для валидации положительных чисел"""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value < 0:
            return ValueError(f"{self.name} не может быть отрицательным")
        setattr(instance, self.name, value)

class CachedProperty:
    """Дескриптор для кэширования вычислений"""

    def __init__(self, func):
        self.func = func
        self.name = self.func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self

        cache_attr = f"_cached_{self.name}"
        if hasattr(instance, cache_attr):
            print("Возвращаем из кэша")
            return getattr(instance, cache_attr)

        value = self.func(instance)
        setattr(instance, cache_attr, value)
        print("Расчитываем и сохраняем в атрибут результат")
        return value

