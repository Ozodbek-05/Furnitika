from django.urls import path
from apps.accounts.views import RegisterCreateView, LoginFormView, ConfirmEmailView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('confirmation/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirmation'),
    # path('profile/', RegisterCreateView.as_view, name='register'),
    # path('resend/code/', RegisterCreateView.as_view, name='register'),
    # path('forget/password', RegisterCreateView.as_view, name='register'),
    # path('update/password', RegisterCreateView.as_view, name='register'),
]