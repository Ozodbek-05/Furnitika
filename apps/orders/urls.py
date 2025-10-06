from django.urls import path
from apps.orders.views import CheckoutCreateView, ProceedToPaymentView, payment_page, process_payment

app_name = 'orders'

urlpatterns = [
    # Checkout sahifasi
    path('', CheckoutCreateView.as_view(), name='create'),

    # Proceed-to-Payment tugmasi uchun
    path('proceed/', ProceedToPaymentView.as_view(), name='proceed_to_payment'),

    # Payment sahifasi
    path('<str:unique_id>/payment/', payment_page, name='payment_page'),

    # Paymentni yakunlash
    path('<str:unique_id>/payment/process/', process_payment, name='process_payment'),
]
