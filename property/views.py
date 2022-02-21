from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Address, PropertyImage, PropertyType, BuildYear, Property, Status
from .thread_methods import address_creator, build_year_creator, image_uploader
from django.contrib import messages
import threading
from django.conf import settings

# Handler for property form (Requires Logged in User)
@login_required
def property_form(request):
    # If the form has been submitted
    if request.method == "POST":
        thread_list = []    # List created to store instance ids to compensate for threads not able to return instances
        # Try to create an address, build year and upload image in seperate threads
        try:
            address_creation_thread = threading.Thread(target = address_creator(request, thread_list))
            build_year_thread = threading.Thread(target = build_year_creator(request, thread_list))
            image_upload = threading.Thread(target = image_uploader(request, thread_list))
            address_creation_thread.start()
            build_year_thread.start()
            image_upload.start()
            address_creation_thread.join()
            build_year_thread.join()
            image_upload.join()
        except Exception as e:
            print(e)
        try:
            # Try to create the property using details from form and threads
            property = Property.objects.create_property(
                request.POST.get('description'), request.POST.get('price'), request.POST.get('footage'), request.POST.get('bathroom_amount'), 
                request.POST.get('bedroom_amount'), request.POST.get('bid_end'), request.user, PropertyType.objects.get(pk = request.POST.get('property_type')), 
                BuildYear.objects.get(pk = thread_list[1]), Status.objects.get(status = 'Active Bid'), Address.objects.get(pk = thread_list[0])
            )
            # Images uploaded prior to property saved. Property linked to its images below
            try:
                for image in range(2, len(thread_list)):
                    print(f"Loop INDEX: {thread_list[image]}")
                    image_ref = PropertyImage.objects.get(pk = thread_list[image])
                    image_ref.property = property
                    image_ref.save()
            except Exception as e:
                print(e)
            messages.success(request, "Property Listing Created")
        except Exception as e:
            print(e)
        return render(request, "properties.html", {'properties': Property.objects.all()})
    # Display the form for a get request
    property_types = PropertyType.objects.all().order_by('property_type')
    return render(request, "property_form.html", {'property_types': property_types})

# View all listed properties
def view_properties(request):
    try:
        return render(request, "properties.html", {'properties': Property.objects.all(), 'bucket': settings.IMAGE_BUCKET_URL})
    except:
        messages.error(request, "Unable to retrieve property listings")
        return render(request, "properties.html")

# View a specific property
def view_property(request, property_id):
    #s3_bucket_url =  settings.INSTRUMENT_IMAGE_URL
    # Retrieve the selected properties details
    property = Property.objects.get(pk=property_id)
    # #If the request is a post request it signals a comment was posted
    # if request.method == "POST":
    #     #If the user is logged in, create a comment instance
    #     if request.user.is_authenticated:
    #         try:
    #             comment = InstrumentComment()
    #             comment.instrument = product
    #             comment.user = request.user
    #             comment.comment = request.POST.get('comment')
    #             comment.save()
    #             messages.info(request, "Comment Posted!")
    #         except:
    #             messages.info(request, "Unable to post comment")
    return render(request, "property.html", {'property': property})
