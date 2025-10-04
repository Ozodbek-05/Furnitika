from django.urls import path
from .views import ProductFilterView, ProductDetailView

app_name = "products"

urlpatterns = [
    path("", ProductFilterView.as_view(), name="home"),
    path("filter/<str:filter_type>/<int:pk>/", ProductFilterView.as_view(), name="filter"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
]
