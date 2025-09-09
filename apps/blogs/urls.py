from django.urls import path
from apps.blogs.views import blog_list_view, blog_detail_view

app_name = 'blogs'

urlpatterns = [
    path('', blog_list_view, name='list'),
    path('<int:pk>/', blog_detail_view, name='detail'),
]