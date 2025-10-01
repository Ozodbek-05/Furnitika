from django.urls import path

from apps.accounts.views import RegisterCreateView, LoginFormView, ConfirmEmailView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('confirmation/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirmation'),
]