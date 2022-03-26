from django.urls import path
from . import views

urlpatterns = [
    #path('login/', views.login, name = 'login_form'),  #no longer needed as AWS COGNITO is responsible for login
    #path('register/', views.register, name = 'registration_form'), ##no longer needed as AWS COGNITO is responsible for registration
    path('logout/', views.logout, name="logout"),
]