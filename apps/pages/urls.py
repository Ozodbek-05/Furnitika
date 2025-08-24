from django.urls import path
from apps.pages.views import home_view, contact_view, blog_view, blog_list_view

app_name = 'pages'

urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('blog-detail/', blog_view, name='detail'),
    path('blog-list/', blog_list_view, name='list'),

]