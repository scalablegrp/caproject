from django.shortcuts import render, redirect
from django.db import transaction
from property.models import Property
from django.contrib import messages

# Create your views here.

# Function to allow users to place a bid
def place_bid(request, property_id):
    try:
        # Get the correct property and update its price to amount in form
        property = Property.objects.get(pk=property_id)
        bid_amount = float(request.POST.get('bid_amount'))
        # Ensure the bid amount submitted is higher than existing highest bid
        if(bid_amount>property.price):
            # Django select_for update method will lock property price until function finishes
            Property.objects.select_for_update(of = ('price')).filter(pk = property_id)
            with transaction.atomic():
                property.price = bid_amount
                property.save()
            messages.success(request, f"Successfull Bid of €{bid_amount}")
        else:
            messages.success(request, f"There is an existing bid higher than {bid_amount}")
    except Exception as e:
            print(e)
    return redirect('property:view_properties')