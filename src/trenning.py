class ValidatDescriptor:
    """Дескриптор для валидации"""
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} не может быть отрицательным")
        setattr(instance, self.name, value)


class SomeClass:
    value = ValidatDescriptor('_value')
    def __init__(self, value):
        self.value = value


a = SomeClass(10)

print(a.value) # 10
a.value = -10 # ValueError: _value не может быть отрицательным
print(a.value)
