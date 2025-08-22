from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:order_id>/', views.create_payment, name='create_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('webhook/', views.yookassa_webhook, name='webhook'),
]