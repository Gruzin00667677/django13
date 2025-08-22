from yookassa import Configuration, Payment
import uuid
from django.conf import settings

# Настройка ключей
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_yookassa_payment(order, return_url):
    """Создание платежа в ЮKassa"""
    payment = Payment.create({
        "amount": {
            "value": str(order.total_price),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "capture": True,
        "description": f"Заказ №{order.id}",
        "metadata": {
            "order_id": order.id
        }
    }, idempotency_key=str(uuid.uuid4()))

    return payment