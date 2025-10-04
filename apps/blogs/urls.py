from django.urls import path
from apps.blogs.views import BlogDetailView, BlogListView, BlogFilterView
app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='blogs_home'),
    path("<int:pk>/", BlogDetailView.as_view(), name="detail"),
    path("filter/<str:filter_type>/<int:pk>/", BlogFilterView.as_view(), name="blog_filter"),
]