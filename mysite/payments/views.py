from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from yookassa.domain.notification import WebhookNotification
from .models import Payment
from orders.models import Order  # Импортируйте вашу модель заказа
from .services import create_yookassa_payment


def create_payment(request, order_id):
    """
    Создает платеж в ЮKassa и перенаправляет пользователя на платежную форму
    """
    try:
        # Получаем заказ или возвращаем 404
        order = get_object_or_404(Order, id=order_id)

        # Проверяем, не был ли заказ уже оплачен
        if order.is_paid:
            return render(request, 'payments/error.html', {
                'error': 'Этот заказ уже оплачен'
            })

        # Создаем платеж в ЮKassa через сервис
        return_url = request.build_absolute_uri('/payments/success/')
        yookassa_payment = create_yookassa_payment(
            order=order,
            return_url=return_url
        )

        # Сохраняем платеж в нашей базе
        payment = Payment.objects.create(
            order=order,
            payment_id=yookassa_payment.id,
            amount=order.total_price,
            status='pending'
        )

        # Перенаправляем пользователя на страницу оплаты ЮKassa
        return redirect(yookassa_payment.confirmation.confirmation_url)

    except Exception as e:
        # Логируем ошибку (на практике используйте logging)
        print(f"Ошибка при создании платежа: {e}")
        return render(request, 'payments/error.html', {
            'error': 'Произошла ошибка при создании платежа'
        })


@csrf_exempt
def yookassa_webhook(request):
    """
    Обработчик вебхуков от ЮKassa (для изменения статусов платежей)
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    try:
        # Получаем и проверяем подпись (для продакшна)
        signature = request.headers.get('Content-Signature')
        # В реальном проекте нужно проверить подпись!
        # if not verify_signature(request.body, signature):
        #     return HttpResponseBadRequest("Invalid signature")

        # Парсим уведомление
        payload = request.body.decode('utf-8')
        notification = WebhookNotification(payload)

        # Обрабатываем только успешные платежи
        if notification.event == 'payment.succeeded':
            payment_info = notification.object

            # Получаем ID платежа из ЮKassa
            yookassa_payment_id = payment_info.id

            # Находим соответствующий платеж в нашей базе
            try:
                payment = Payment.objects.get(payment_id=yookassa_payment_id)

                # Проверяем сумму для безопасности
                if float(payment_info.amount.value) != float(payment.amount):
                    payment.status = 'amount_mismatch'
                    payment.save()
                    return HttpResponse("Amount mismatch", status=400)

                # Обновляем статус платежа
                payment.status = 'succeeded'
                payment.save()

                # Обновляем статус заказа
                order = payment.order
                order.is_paid = True
                order.save()

            except Payment.DoesNotExist:
                # Логируем отсутствие платежа
                print(f"Платеж {yookassa_payment_id} не найден в базе")
                return HttpResponse("Payment not found", status=404)

        # Обрабатываем отмененные платежи
        elif notification.event == 'payment.canceled':
            payment_info = notification.object
            try:
                payment = Payment.objects.get(payment_id=payment_info.id)
                payment.status = 'canceled'
                payment.save()
            except Payment.DoesNotExist:
                pass

        return HttpResponse(status=200)

    except Exception as e:
        # Логируем ошибку
        print(f"Ошибка обработки вебхука: {e}")
        return HttpResponse(status=500)


def payment_success(request):
    """
    Страница успешной оплаты
    """
    return render(request, 'payments/success.html')


def payment_error(request):
    """
    Страница ошибки оплаты
    """
    return render(request, 'payments/error.html')