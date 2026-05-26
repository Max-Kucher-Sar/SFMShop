from models.delivery import Delivery, ExpressDelivery, StandardDelivery
from models.notifications import Notification, SMSNotification, EmailNotification

express = ExpressDelivery()
standart = StandardDelivery()

def deliver_processing(object: Delivery, distance: float) -> float:
    return object.calculate_cost(distance)

sms = SMSNotification()
email = EmailNotification()

def send_notification(object: Notification, message: str):
    object.send(message)

send_notification(sms, "С Днем Рождения!")
send_notification(email, "С Новым Годом!")