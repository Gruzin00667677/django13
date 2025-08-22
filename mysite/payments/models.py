from django.db import models

# Create your models here.
from django.db import models
from orders.models import Order  # Импортируйте вашу модель заказа


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает оплаты'),
        ('succeeded', 'Успешно'),
        ('canceled', 'Отменен'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField("ID платежа ЮKassa", max_length=100)
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    def __str__(self):
        return f"Платеж {self.payment_id} для заказа {self.order.id}"