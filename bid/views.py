from django.shortcuts import render, redirect
from django.db import transaction
from property.models import Property
from .models import Bid
from django.contrib import messages
from .sns_utils import sns

# Create your views here.

# Function to allow users to place a bid
def place_bid(request, property_id):
    try:
        # Get the correct property and update its price to amount in form
        property = Property.objects.get(pk=property_id)
        bid_amount = float(request.POST.get('bid_amount'))
        successful_transaction = False
        # Ensure the bid amount submitted is higher than existing highest bid AND the bid hasn't timed out
        if(bid_amount>property.price and property.calc_remaining_bid_time() != "Bid End"):
            # Django select_for update method will lock property price until function finishes (Optimistic locking)
            Property.objects.select_for_update(of = ('price')).filter(pk = property_id)
            with transaction.atomic():
                user_email = request.user.email
                sns.topic_subscribe(f"BidNotificationForPropertyId{property_id}", user_email)
                print("I am called")
                # Check if the bidder already has a bid on the property
                if Bid.objects.filter(property=property).filter(user = request.user):
                    # Get the users existing bid and update with new bid value
                    try:
                        bid = Bid.objects.get(property=property, user = request.user)
                        bid.amount = bid_amount
                        bid.save()
                    except Exception as e:
                        print(e)
                        return
                else:
                    # If the bidder doesn't already have a bid for the property instantiate the Bid class
                    try:
                        Bid.objects.create_bid(property, request.user, bid_amount)
                        # Bidder will not be signed up to sns topic if they haven't already created a bid

                        # try:
                        #     sns.topic_subscribe(f"BidNotificationForPropertyId{property_id}", user_email)
                        # except Exception as e:
                        #     print(e)
                        #     return
                    except Exception as e:
                        print(e)
                        return
                successful_transaction = True   #If code runs till this line the transaction has been a successs and property price can be updated
            if successful_transaction:
                property.price = bid_amount
                property.save()
                messages.success(request, f"Successfull Bid of €{bid_amount}")
            else:
                messages.info(request, f"There was an issue logging your bid")
        else:
            messages.success(request, f"Your bid must be higher than {bid_amount}")
    except Exception as e:
            print(e)
    return redirect('property:view_properties')