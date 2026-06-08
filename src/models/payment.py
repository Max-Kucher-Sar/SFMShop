from abc import ABC, abstractmethod
from .mixins import LoggableMixin, SerializableMixin

class PaymentMethod(ABC):
    def __init__(self, payment_method):
        self.payment_method = payment_method

    @abstractmethod
    def process_fee(self, amount: float):
        """Расчет комисии"""
        pass

    @abstractmethod
    def amount_transfer(self, amount: float):
        """Метод перевода"""
        pass

class CardPayment(LoggableMixin, SerializableMixin, PaymentMethod):
    def __init__(self):
        self.payment_method = 'card'
        super().__init__(self.payment_method)
        self.log(f"Создан платеж card")

    def process_fee(self, amount: float) -> float:
        """Расчет комисии"""
        if amount > 10000:
            fee = amount * 0.02
        else:
            fee = amount * 0.03
        return fee

    def amount_transfer(self, amount: float) -> float:
        """Метод перевода"""
        fee = self.process_fee(amount)
        result = amount + fee
        print(f"Зарядка карты на сумму {result}")
        return True

class PayPalPayment(PaymentMethod):
    def __init__(self):
        self.payment_method = 'card'
        super().__init__(self.payment_method)

    def process_fee(self, amount: float) -> float:
        """Расчет комисии"""
        return amount * 0.035

    def amount_transfer(self, amount: float) -> float:
        """Метод перевода"""
        fee = self.process_fee(amount)
        result = amount + fee
        print(f"Зарядка PayPal на сумму {result}")
        return True

class BankTransferPayment(PaymentMethod):
    def __init__(self):
        self.payment_method = 'card'
        super().__init__(self.payment_method)

    def process_fee(self, amount: float) -> int:
        """Расчет комисии"""
        return 50

    def amount_transfer(self, amount: float) -> float:
        """Метод перевода"""
        fee = self.process_fee(amount)
        result = amount + fee
        print(f"Банковский перевод на сумму {result}")
        return True

class Payment:
    def __init__(self, order_id: int, amount: int, payment_method: str):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = "pending"

print(CardPayment.mro())