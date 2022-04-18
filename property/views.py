from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Address, PropertyImage, PropertyType, BuildYear, Property, Status
from .thread_methods import address_creator, build_year_creator, property_creator, image_uploader, sns_topic_creator
from django.contrib import messages
import threading
from django.conf import settings
#from lib_ideas.methods import MyLibMethods

# Handler for property form
def property_form(request):
    # Requires a logged in user, Auth using Cognito, if 'cognito_details' in session user is logged in
    if len(request.session.get('cognito_details', {})) == 0:
        messages.info(request, "You need to login/register to post a property for sale")
        return redirect("https://scalable.auth.us-east-1.amazoncognito.com/login?client_id=6bghvg18tkkiarbqpekpfgij78&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=http://localhost:8080")
    # If the form has been submitted
    if request.method == "POST":
        print("Called")
        thread_list = []    # List created to store instance ids to compensate for threads not able to return instances
        # Try to create an address, build year, property instances and upload image in seperate threads
        try:
            address_creation_thread = threading.Thread(target = address_creator(request, thread_list))
            build_year_thread = threading.Thread(target = build_year_creator(request, thread_list))
            property_creation_thread = threading.Thread(target = property_creator(request, thread_list))
            image_upload = threading.Thread(target = image_uploader(request, thread_list))
            address_creation_thread.start()
            build_year_thread.start()
            property_creation_thread.start()
            topic_status = ['topic_status']  # List passed to thread to track user notification status 
            #Check if user wants to receive notifications on bids
            if request.POST.get('trackBid') == 'true':
                # If the correct aws keys arent provided the topic will not be created, thread parameter value will be adjusted to True if successful
                sns_topic_thread = threading.Thread(target = sns_topic_creator(request, thread_list, topic_status))
                sns_topic_thread.start()
            image_upload.start()
            address_creation_thread.join()
            build_year_thread.join()
            property_creation_thread.join()
            image_upload.join()
            if request.POST.get('trackBid') == 'true':
                sns_topic_thread.join()
            # If a sns topic was created inform the user on its status
            if topic_status[0] == True:
                messages.success(request, "Property listing created. You will receive notifications anytime a bid is made")
            elif topic_status[0] == False:
                messages.error(request, "Property Listing created but an issue caused an error in receiving bidding notification has occured")
            else:
                # User may not have opted to receive notifications
                messages.success(request, "Property Listing Created")
        except Exception as e:
            print(e)
            messages.error(request, "Unable to create property")
        return redirect('property:view_properties')
    # Display the form for a get request
    property_types = PropertyType.objects.all().order_by('property_type')
    return render(request, "property_form.html", {'property_types': property_types})

# View all listed properties
def view_properties(request):
    try:
        properties = list(Property.objects.all())
        # If the request is a post request it identifies the user either wants to sort or filter the properties
        # if request.method == "POST":
        #     try:
        #         # Determine if the user selected a valid sort/filter option
        #         if not (request.POST.get('filter') or request.POST.get('sort_by')):
        #             messages.info(request, "You have tried to filter/sort without selecting any of the options available")
        #         else:
        #             # Instantiate the library for including sort functionality
        #              my_lib = MyLibMethods()
        #              if request.POST.get('sort_by') == 'price_low_to_high':
        #                 try:
        #                     my_lib.sort_by(properties, 0, len(properties)-1, 'price', 'ascending')
        #                 except Exception as e:
        #                     print(e)
        #              if request.POST.get('sort_by') == 'price_high_to_low':
        #                 try:
        #                     my_lib.sort_by(properties, 0, len(properties)-1, 'price', 'descending')
        #                 except Exception as e:
        #                     print(e)
        #         # If a user wants to filter, sorting has to be done prior to filtering because of binary sort use
        #         # Sort the options based on the submitted forms values
        #     except Exception as e:
        #         print(e)                 
        if len(properties) <= 0:
            messages.info(request, "No properties in Database")
        return render(request, "properties.html", {'properties': properties, 'bucket': settings.IMAGE_BUCKET_URL})
    except Exception as e:
        print(e)
        messages.error(request, "Unable to retrieve property listings")
        return render(request, "error.html")

# View a specific property
def view_property(request, property_id):
    #s3_bucket_url =  settings.INSTRUMENT_IMAGE_URL
    # Retrieve the selected properties details
    property = Property.objects.get(pk=property_id)
    return render(request, "property.html", {'property': property, 'bucket': settings.IMAGE_BUCKET_URL})

