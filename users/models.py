from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    current_shop = models.IntegerField()

class Shop(models.Model):
    # make client_id and api_key unique
    client_id = models.IntegerField(unique=True)
    api_key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.client_id)
