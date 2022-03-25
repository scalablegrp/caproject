from django.contrib import admin
from .models import PropertyType, Property, Status

# Register your models here.
admin.site.register(PropertyType)
admin.site.register(Property)
admin.site.register(Status)