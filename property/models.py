from django.db import models
import datetime
from django.apps import apps

# Create your models here
class PropertyType(models.Model):
    property_type = models.CharField(max_length = 100)

# BuildYearManager will allow BuildYear instances to be initiated using constructor
class BuildYearManager(models.Manager):
    def create_build_year(self, build_year):
        build_year = self.create(build_year = build_year)
        return build_year

class BuildYear(models.Model):
    build_year = models.SmallIntegerField()
    objects = BuildYearManager()   # BuildYearManager object allows constructor to bbe utilised for creating a build year

class Status(models.Model):
    status = models.CharField(max_length = 25)

# AddressManager will allow address instances to be initiated using constructor
class AddressManager(models.Manager):
    def create_address(self, house_number, street, town, county, postcode):
        address = self.create(house_number = house_number, street = street, town = town, county = county, postcode = postcode)
        return address

class Address(models.Model):
    house_number = models.CharField(max_length = 100)
    street = models.CharField(max_length = 100)
    town = models.CharField(max_length = 100)
    county = models.CharField(max_length = 100)
    postcode = models.CharField(max_length = 10)
    objects = AddressManager()   # Address Manager object allows constructor to bbe utilised for creating an address

    #Meta class for enusuring rows are unique for addresses
    class Meta:
        unique_together = ['house_number', 'street', 'town', 'county', 'postcode']

# PropertyManager will allow address instances to be initiated using constructor
class PropertyManager(models.Manager):
    def create_property(self, description, price, square_footage, bathroom_amount, bedroom_amount, bid_end, posted_by, property_type, build_year, status, address):
        try:
            property = self.create(
                description = description, price = price, square_footage = square_footage, bathroom_amount = bathroom_amount, bedroom_amount = bedroom_amount, 
                bid_end = bid_end, posted_by = posted_by, property_type = property_type, build_year = build_year, status = status, address = address
            )
            property.save()
            return property
        except Exception as e:
            print(e)

class Property(models.Model):
    description = models.CharField(max_length = 1000)
    price = models.FloatField()
    square_footage = models.FloatField()
    bathroom_amount = models.IntegerField()
    bedroom_amount = models.IntegerField()
    bid_end = models.DateTimeField()
    posted_by = models.CharField(max_length = 60)
    property_type = models.ForeignKey(PropertyType, on_delete = models.CASCADE)
    build_year = models.ForeignKey(BuildYear, on_delete = models.CASCADE)
    status = models.ForeignKey(Status, on_delete = models.CASCADE)
    address = models.ForeignKey(Address, on_delete = models.CASCADE)
    objects = PropertyManager() # Property Manager object allows constructor to be utilised for creating a property

    # Get property images
    def get_image(self):
        return PropertyImage.objects.filter(property = self.id)  

    # Check if the bid is still active
    def is_bid_active(self):
        # If the bid deadline time has been reached return False, if bid is still active return true
        if (self.bid_end - datetime.datetime.now()).total_seconds() <= 0:
            return False
        return True

    # Maybe implement this in library (def calc_time_between)
    def calc_remaining_bid_time(self):
        # If the bid hasn't already ended, get the amount of ramaining time in seconds
        if self.is_bid_active():
            difference = int((self.bid_end - datetime.datetime.now()).total_seconds())
            return difference
        return "Bid End"

    # Convert the remaining time to day,hour,minute,second format
    def specific_time_details(self):
        # Check there is still time remaining in the bid
        if self.is_bid_active():
            difference = int((self.bid_end - datetime.datetime.now()).total_seconds())
            days = difference // 86400 or 0
            difference -= days * 86400
            hours = (difference // 3600) % 24 
            difference -= hours * 3600;    
            mins = difference // 60 or 0 
            difference -= mins * 60 or 0
            return f"{days} day(s), {hours} hour(s), {mins} min(s), {difference} second(s)"
        return "Bid End"
    
    # Method to identify  highest bidder
    def identify_highest_bidder(self):
        bid_model = apps.get_model('bid.Bid')   # This method allows the Bid model to be imported from bid app without circular import error
        # Get the largest amount from the bids for the property and return bidder email address
        highest_bidder = bid_model.objects.filter(property = self.id).latest('amount')
        return highest_bidder.user

    def get_sorting_filter(self, sorting_filter):
        if sorting_filter == "price":
            return self.price

    def is_purchased(self):
        if self.status == Status.objects.get(status = 'Purchased'):
            return True

    # # Meta class for enusuring rows are unique for properties
    # class Meta:
    #     unique_together = [
    #         'description', 'price', 'square_footage', 'bathroom_amount', 'bedroom_amount', 'bid_end', 'posted_by', 'property_type', 'build_year', 'status', 'address' 
    #     ]

# ImageManager will allow PropertyImage instances to be initiated using constructor
class ImageManager(models.Manager):
    def create_property_image(self, image, property_id):
        try:
            image = self.create(
                image = image, property = Property.objects.get(pk=property_id)
            )
            image.save()
        except Exception as e:
            print(e)

# This function will be used to assign uploaded image paths based on their corresponding property id
def image_upload_path(instance, file_name):
    try:
        return f"properties/property{instance.property.id}/{file_name}"
    except Exception as e:
        print(e)

class PropertyImage(models.Model):
    image = models.FileField(upload_to=image_upload_path)   # image will be stored in path of properties/propertyid/filename
    property = models.ForeignKey(Property, on_delete = models.CASCADE, null = True)
    objects = ImageManager() # Image Manager object allows constructor to be utilised for creating a property


