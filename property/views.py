from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Address, PropertyImage, PropertyType, BuildYear, Property, Status
from .thread_methods import address_creator, build_year_creator, property_creator, image_uploader
from django.contrib import messages
import threading
from django.conf import settings

# Handler for property form (Requires Logged in User)
@login_required
def property_form(request):
    # If the form has been submitted
    if request.method == "POST":
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
            image_upload.start()
            address_creation_thread.join()
            build_year_thread.join()
            property_creation_thread.join()
            image_upload.join()
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
        properties = Property.objects.all()
        if not properties.exists():
            messages.info(request, "No properties in Database")
        return render(request, "properties.html", {'properties': properties, 'bucket': settings.IMAGE_BUCKET_URL})
    except:
        messages.error(request, "Unable to retrieve property listings")
        return render(request, "properties.html")

# View a specific property
def view_property(request, property_id):
    #s3_bucket_url =  settings.INSTRUMENT_IMAGE_URL
    # Retrieve the selected properties details
    property = Property.objects.get(pk=property_id)
    return render(request, "property.html", {'property': property})

