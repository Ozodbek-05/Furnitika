from django.urls import path
from apps.blogs.views import BlogDetailView, BlogListView, BlogFilterView, BlogSearchView

app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='blogs_home'),
    path("search/", BlogSearchView.as_view(), name="search"),
    path("<int:pk>/", BlogDetailView.as_view(), name="detail"),
    path("filter/<str:filter_type>/<int:pk>/", BlogFilterView.as_view(), name="blog_filter"),
]


