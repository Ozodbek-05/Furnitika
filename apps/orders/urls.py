from django.urls import path
from apps.orders.views import CheckoutCreateView

app_name = 'orders'

urlpatterns = [
    path('', CheckoutCreateView.as_view(), name='create'),
]
