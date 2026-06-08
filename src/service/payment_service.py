from abc import ABC, abstractmethod

class PaymentValidator:
    """Класс валидирует данные"""
    @staticmethod
    def validate_payment(payment: Payment):
        """Валидация платежа"""
        if payment.amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if payment.payment_method not in ["card", "paypal", "bank_transfer"]:
            raise ValueError("Неизвестный метод оплаты")
        return True


class PaymentRepo:
    def __init__(self, payment: Payment):
        self.payment = payment

    def save_to_database(self, database: Database):
        database.save(self.payment)
        return True

class NotificationService(ABC):
    """Интерфейс для уведомлений"""
    @abstractmethod
    def send(self, payment: Payment):
        pass

class EmailNotification(NotificationService):
    def send(self, payment: Payment):
        print(f"Отправка email о платеже {payment.order_id}")

class PaymentProcessor:
    def __init__(
            self, payment_method: PaymentMethod,
            database: Database,
            notification_service: NotificationService
    ):
        self.payment_method = payment_method
        self.database = database
        self.notification_service = notification_service

    def process_payment(self, payment: Payment):
        #Валидируем
        PaymentValidator().validate_payment(payment)

        #Если ошибок нет, обрабатываем платеж
        is_success = self.payment_method.amount_transfer(payment.amount)
        if is_success:
            payment.status = "completed"
        else:
            payment.status = "failed"
            raise ValueError(f"Ошибка обработки платежа методом {self.payment_method.payment_method}")

        #Сохраняем в базу данных
        PaymentRepo(payment).save_to_database(self.database)

        #Отсылаем уведомление
        self.notification_service.send(payment)
        return payment.status
