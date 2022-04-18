from .models import Address, BuildYear, PropertyImage, Property, Status, PropertyType
from bid.sns_utils import sns
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

def property_creator(request, thread_list):
    try:
        # Initilize a property, save it to db and put its id in thread_list argument for reference in S3 image path
        property = Property.objects.create_property(
            request.POST.get('description'), request.POST.get('price'), request.POST.get('footage'), request.POST.get('bathroom_amount'), 
            request.POST.get('bedroom_amount'), request.POST.get('bid_end'), request.session['cognito_details']['email'], PropertyType.objects.get(pk = request.POST.get('property_type')), 
            BuildYear.objects.get(pk = thread_list[1]), Status.objects.get(status = 'Active Bid'), Address.objects.get(pk = thread_list[0])
        )
        thread_list.append(property.id)      
    except Exception as e:
        print(e)


def sns_topic_creator(request, thread_list, topic_status):
    # Try to create a sns topic for the property
    try:
        # The created property will always be index 2
        sns.topic_subscribe(f"BidNotificationForPropertyId{thread_list[2]}", request.session['cognito_details']['email'])
        topic_status[0] = True
    except Exception as e:
        topic_status[0] = False



def image_uploader(request, thread_list):
    # Upload the image to S3 and instantiate PropertyImage. Id put into threadlist to retrieve instance for assigning property when saved
    try:
        # Traverse all uploaded images and create PropertyImage instances using a reference to property id contained in threadlist
        for i in request.FILES.getlist('image'):
            try:
                image_index = 2
                image = PropertyImage.objects.create_property_image(i, thread_list[image_index])
                image_index+=1
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)