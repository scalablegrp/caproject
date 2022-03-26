from django.db import models
from property.models import Property



# Create your models here.

# BidManager will allow Bid instances to be initiated using constructor
class BidManager(models.Manager):
    def create_bid(self, property, user, amount):
        bid = self.create(property = property, user = user, amount = amount)
        bid.save()

class Bid(models.Model):
    # Django doesn't support composite keys so unique_together in Meta class ensures no duplicate rows for property and user attributes
    property = models.ForeignKey(Property, null=False, on_delete=models.CASCADE)
    user = models.CharField(max_length = 60)
    amount = models.FloatField()
    objects = BidManager()   # BuildYearManager object allows constructor to be utilised for creating a bid

    class Meta:
        managed = True
        unique_together = [['property', 'user']]




