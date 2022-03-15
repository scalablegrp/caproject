from django.urls import path
from . import views


urlpatterns = [
    path('', views.display_home_page, name = 'home'),
    path('error', views.display_error_page, name = 'error'),
]