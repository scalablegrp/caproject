from django.urls import path
from . import views

app_name = 'bid'
urlpatterns = [
    path('place_bid/<int:property_id>', views.place_bid, name = 'place_bid'),
    path('view_bids', views.view_bids, name = 'view_bids'),
]
