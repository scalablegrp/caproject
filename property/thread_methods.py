from .models import Address, BuildYear, PropertyImage
from django.conf import settings

def address_creator(request, thread_list):
    try:
        # Initilize an address, save it to db and put its id in thread_list argument
        address = Address.objects.create_address(
                    request.POST.get('house_number'), request.POST.get('street'), request.POST.get('town'), request.POST.get('county'), request.POST.get('post_code')
                )
        address.save()
        thread_list.append(address.id)      
    except Exception as e:
        print(e)

def build_year_creator(request, thread_list):
    # If the build year exists already in the database
    if BuildYear.objects.filter(build_year = request.POST.get('build_year')):
        # Try to get the build year instance id and put in thread_list argument
        try:
            build_year = BuildYear.objects.get(build_year = request.POST.get('build_year'))
            thread_list.append(build_year.id)
        except Exception as e:
            print(e)
        return
    # Create a new record for the build year if it doesn't already exist and put its id into the thread_list
    try:
        build_year = BuildYear.objects.create_build_year(request.POST.get('build_year'))
        build_year.save()
        thread_list.append(build_year.id)
    except Exception as e:
        print(e)

def image_uploader(request, thread_list):
    # Upload the image to S3 and instantiate PropertyImage. Id put into threadlist to retrieve instance for assigning property when saved
    try:
        # Traverse all uploaded images and create PropertyImage instances 
        for i in request.FILES.getlist('image'):
            image = PropertyImage.objects.create_property_image(i)
            thread_list.append(image.id)    # Thread list to keep a reference of image id's 
    except Exception as e:
        print(e)