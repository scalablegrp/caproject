from django.urls import path
from . import views


app_name = 'payment'
urlpatterns = [
    path('property/<int:property_id>', views.direct_to_payment_form, name = 'make_payment'),
    path('my_purchases', views.view_purchases, name = 'view_purchases'),
    path('status/<int:property_id>/<str:status>', views.payment_status, name = 'payment_status'),
]