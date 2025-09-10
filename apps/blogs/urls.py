from django.urls import path
from apps.blogs.views import blog_list_view, blog_detail_view
from . import views
app_name = 'blogs'

urlpatterns = [
    path('', blog_list_view, name='blogs_home'),
    path('<int:pk>/', blog_detail_view, name='detail'),
    path("filter/<str:filter_type>/<int:pk>/", views.blog_filter_view, name="blog_filter"),
]