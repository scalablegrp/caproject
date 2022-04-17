from django.db import models
from property.models import Property

class PurchaseManager(models.Manager):
    # Constructor for Purchase instances
    def create_purchase(self, user_email, property):
        try:
            purchase = self.create(
                user = user_email, cost = property.price, property = property
            )
            return purchase
        except Exception as e:
            print(e)

class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    cost = models.FloatField()
    user = models.CharField(max_length = 200)
    property = models.ForeignKey(Property, null = False, on_delete = models.PROTECT)
    objects = PurchaseManager() # Property Manager object allows constructor to be utilised for creating a property

    # Meta class for enusuring only one payment per user per property
    class Meta:
        unique_together = [
           'property', 'user'
         ]
