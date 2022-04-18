from django.shortcuts import render, redirect
from django.db import transaction
from property.models import Property
from .models import Bid
from django.contrib import messages
from .thread_methods import create_queue, sns_topic_creator, bid_creator, publish_new_bid
import threading

# Create your views here.

# Function to allow users to place a bid
def place_bid(request, property_id):
    # Requires a logged in user, Auth using Cognito, if 'cognito_details' in session user is logged in
    if len(request.session.get('cognito_details', {})) == 0:
        messages.info(request, "You need to login/register to bid")
        return render(request, "error.html")
    try:
        property = Property.objects.get(pk=property_id)
        bid_amount = float(request.POST.get('bid_amount'))
        # Ensure the bid amount submitted is higher than existing highest bid AND the bid hasn't timed out
        if(bid_amount>property.price and property.calc_remaining_bid_time() != "Bid End"):
            successful_transaction = [False, property_id]   # The bid instantiator needs a property id and status passed to its thread as a listus 
            sns_thread_list = [property_id, 'topic_status'] # List to pass to thread containing details of property 
            bid_creator_thread = threading.Thread(target = bid_creator(request, successful_transaction))
            # Django select_for update method will lock property price until function finishes (Optimistic locking)
            Property.objects.select_for_update(of = ('price')).filter(pk = property_id)
            with transaction.atomic():
                try:
                    bid_creator_thread.start()
                    #Check if user wants to receive notifications on bids
                    queue = create_queue()
                    if request.POST.get('trackBid') == 'true':
                        try:
                            # If thread is successful  its parameter value will be adjusted to True if successful
                            sns_topic_thread = threading.Thread(target = sns_topic_creator(request, sns_thread_list))
                            sns_topic_thread.start()
                            sns_topic_thread.join()
                        except Exception as e:
                            print(e)
                    bid_creator_thread.join()
                except Exception as e:
                    print(e)
            # If the successful transaction list has a True boolean the bid was succesful
            if successful_transaction[0] == True:
                # Publish to the topic that a new bid was made
                property_id_thread_list = [property_id, False]
                sns_publish_thread = threading.Thread(target = publish_new_bid(request, property_id_thread_list, queue))
                sns_publish_thread.start()
                property.price = bid_amount
                property.save()
                sns_publish_thread.join()
                # If the user chose to receive notifications inform them of status
                if sns_thread_list[1] != 'topic_status':
                    if property_id_thread_list[1] == True:
                        messages.success(request, f"Successfull Bid of €{bid_amount}\nPlease check your email address for notifications")
                    elif property_id_thread_list[1] == False:
                        messages.error(request, f"Successfull Bid of €{bid_amount} but an issue caused an error in receiving bidding notification has occured")
                else:
                    messages.success(request, f"Successfull Bid of €{bid_amount}")
            else:
                messages.info(request, f"There was an issue logging your bid")
        else:
            messages.success(request, f"Your bid must be higher than {bid_amount}")
    except Exception as e:
            print(e)
    return redirect('property:view_properties')

# View all created bids 
def view_bids(request):
    if len(request.session.get('cognito_details', {})) == 0:
        messages.info(request, "You need to login/register to bid")
        return render(request, "error.html")
    else:
        bids = Bid.objects.filter(user = request.session['cognito_details']['email'])
        return render(request, "view_bids.html",{ 'bids' : bids})
