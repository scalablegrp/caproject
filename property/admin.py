from django.contrib import admin
from .models import Status, PropertyType, Property
# Register your models here.
admin.site.register(Property)
admin.site.register(Status)
admin.site.register(PropertyType)