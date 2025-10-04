from django.urls import path

from apps.pages.views import about_view, contact_page_view, home_view, not_found_view


app_name = 'pages'

urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_page_view, name='contact'),
    path('about/', about_view, name='about'),
    path('404/', not_found_view, name = '404'),
    # path('test/', test_contact, name='test')
]