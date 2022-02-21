from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name = 'login_form'),
    path('register/', views.register, name = 'registration_form'),
    path('logout/', views.logout, name="logout"),
]