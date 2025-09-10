from django.urls import path
from . import views

app_name = 'products'


urlpatterns = [
    path('', views.product_filter_view, name='home'),
    path("filter/<str:filter_type>/<int:pk>/", views.product_filter_view, name="filter"),
    path('detail/<int:pk>/', views.product_detail_view, name='product_detail'),
]
