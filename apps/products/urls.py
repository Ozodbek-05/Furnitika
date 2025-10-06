from django.urls import path
from .views import ProductFilterView, ProductDetailView, CommentCreateView, ProductSearchView, LivingRoomProductsView

app_name = "products"

urlpatterns = [
    path("", ProductFilterView.as_view(), name="home"),
    path("search/", ProductSearchView.as_view(), name="search"),
    path("filter/<str:filter_type>/<int:pk>/", ProductFilterView.as_view(), name="filter"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path('living-room/', LivingRoomProductsView.as_view(), name='living_room_products'),
    path("comment/<int:pk>/", CommentCreateView.as_view(), name="comment"),
]