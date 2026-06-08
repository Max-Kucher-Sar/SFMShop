from typing import Optional
from .notifications import Notification
from ..service.database_service import Database
from .user import User
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, balance: float) -> float:
        pass

class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, balance: float) -> float:
        return balance * (1 + self.percent / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, balance: float) -> float:
        return balance + self.amount

class UserCalculator:
    @staticmethod
    def calculate_total_spent(user: User) -> float:
        """Расчет общей потраченной суммы"""
        total = 0
        for order in user.orders:
            total += order.total
        return total

    @staticmethod
    def apply_discount(user: User, discount: Optional[DiscountStrategy] = None) -> float | None:
        """Применение скидки к балансу"""
        return discount.apply(user.balance)


class UserValidator:
    @staticmethod
    def validate_user(user: User):
        if not user.name:
            raise ValueError("Имя не может быть пустым")
        if "@" not in user.email:
            raise ValueError("Email должен содержать @")
        if user.age < 18:
            raise ValueError("Пользователь должен быть старше 18 лет")

class UserRepo:
    def __init__(self, user: User):
        self.user = user

    def save_to_database(self, db: Database):
        db.save(self.user)
        return True

class UserNotif:
    """Класс для описания логики отправки уведомлений"""
    def __init__(self, user: User):
        self.user = user

    def send_welcome_email(self, notification: Notification):
        """Отправка приветственного email"""
        msg = f"Отправка email на {self.user.email}: Добро пожаловать, {self.user.name}!"
        notification.send(msg)

    def generate_report(self, notification: Notification):
        """Генерация отчета"""
        report = f"Пользователь: {self.user.name}\n"
        report += f"Email: {self.user.email}\n"
        report += f"Всего заказов: {len(self.user.orders)}\n"
        report += f"Потрачено: {UserCalculator.calculate_total_spent(self.user)}\n"
        notification.send(report)
        return report


