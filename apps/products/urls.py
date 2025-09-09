from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("cart/", views.product_cart, name="cart"),
    path("checkout/", views.product_checkout, name="checkout"),
    path("<int:pk>/", views.product_detail, name="detail"),

    path("", views.product_grid_sidebar_left, name="grid"),

    path("category/<int:category_id>/", views.product_grid_sidebar_left, name="by_category"),

    path("manufacturer/<int:manufacturer_id>/", views.product_grid_sidebar_left, name="by_manufacturer"),

    path("color/<int:color_id>/", views.product_grid_sidebar_left, name="by_color"),

    path("tag/<int:tag_id>/", views.product_grid_sidebar_left, name="by_tag"),
]
