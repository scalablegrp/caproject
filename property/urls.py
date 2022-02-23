from django.urls import path
from . import views

app_name = 'property'
urlpatterns = [
    path('view_properties', views.view_properties, name = 'view_properties'),
    path('add', views.property_form, name = 'property_form'),
    path('view_property/<int:property_id>', views.view_property, name = 'view_property'),
]