from django.shortcuts import render, redirect,reverse
from django.conf import settings
from .models import Purchase
from property.models import Property, Status
from django.contrib import messages
import stripe


# Create your views here
def direct_to_payment_form(request, property_id):
    # Requires a logged in user, Auth using Cognito, if 'cognito_details' in session user is logged in
    if len(request.session.get('cognito_details', {})) == 0:
        messages.info(request, "You need to login/register to post a property for sale")
        return render(request, "error.html")
    property = Property.objects.get(id=property_id)
    try:
        # If the user is logged in ensure they are the highest bidder and the bid has ended
        if property.identify_highest_bidder() == request.session['cognito_details']['email'] and property.is_bid_active() == False:
            # Create a String with information on the property
            property_info = f"Property @ \n{property.address.house_number},\n{property.address.street},\n{property.address.town},\n{property.address.county},\n{property.address.postcode}"
            # Create a Stipe session containing details on property to be paid for
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_session = stripe.checkout.Session.create(
                line_items = [{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': property_info
                        },
                        'unit_amount': int(property.price * 100)
                    },
                    'quantity': 1,
                }],
                mode = 'payment',
                #If the payment is successful or failed the page which shows all the listed properties will be displayed with a message giving status of payment
                success_url = request.build_absolute_uri(reverse('payment:payment_status', args = [property.id, 'success'])),
                cancel_url = request.build_absolute_uri(reverse('payment:payment_status', args = [property.id,'fail'])),
            )
            return redirect(stripe_session.url, code=303)
    except Exception as e:
        print(e)
        messages.info(request, "An error has occured")
        return render(request, "error.html")

def payment_status(request, property_id,status):
    # Redirect the user to a page with details of their payment status
    try:
        if status == 'fail':
            # Display a message showing the payment has failed if the status is failed
            messages.info(request, "Payment has not gone through")
        elif status == 'success':
            # Change the status of the property
            property = Property.objects.get(id=property_id) 
            property.status =  Status.objects.get(status = 'Purchased')
            property.save()
            # Create a payment Record
            purchase_record = Purchase.objects.create_purchase(request.session['cognito_details']['email'], property)
            purchase_record.save()
            # Display a message showing the payment was successful if it is 
            messages.info(request, "Payment Successful!")
        return redirect('property:view_properties')
    except Exception as e:
        print(e)
        messages.info(request, "An error has occured")
        return (request, 'index.html')

def view_purchases(request):
    # Requires a logged in user, Auth using Cognito, if 'cognito_details' in session user is logged in
    if len(request.session.get('cognito_details', {})) == 0:
        messages.info(request, "You need to login/register to view purchases you have made")
        return render(request, "error.html")
    # If the user is logged in retrieve their purchase details
    try:
        return render (request, "purchases.html", {'purchases': Purchase.objects.filter(user = request.session['cognito_details']['email'])})
    except Exception as e:
        print(e)
        messages.info(request, "An error has occured")
        return redirect('property:view_properties')





