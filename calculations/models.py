from django.db import models
from users.models import Shop

# from analytics.users.models import *
MAX_DIGITS = 8
DECIMAL_PLACES = 1


class Main_analytic(models.Model):
    # user = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    ordered_rub = models.BigIntegerField(null=True)
    ordered_thing = models.IntegerField(null=True)
    ordered_percent_rub = models.IntegerField(null=True)
    ordered_percent_thing = models.IntegerField(null=True)

    redeemed_rub = models.BigIntegerField(null=True)
    redeemed_percent_rub = models.IntegerField(null=True)

    proceeds_rub = models.BigIntegerField(null=True)
    proceeds_percent_rub = models.IntegerField(null=True)


    cancelled_thing = models.IntegerField(null=True)
    cancelled_percent_thing = models.IntegerField(null=True)

    refund_thing = models.IntegerField(null=True)
    refund_percent_thing = models.IntegerField(null=True)

    views_thing = models.IntegerField(null=True)
    views_percent = models.IntegerField(null=True)

    to_cart_thing = models.IntegerField(null=True)
    to_cart_percent = models.IntegerField(null=True)

    shop = models.IntegerField()

class Supplies_info(models.Model):
    warehouse = models.CharField(max_length=50)
    sku = models.CharField(max_length=70)
    product = models.CharField(max_length=200)
    days_left = models.CharField(max_length=30)
    remains = models.BigIntegerField(null=True, default=0)
    total_warehouse_remains = models.BigIntegerField(null=True)
    selling_speed = models.DecimalField(null=True, max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    total_product_selling_speed = models.DecimalField(null=True, max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)

    shop = models.IntegerField()



class ABC(models.Model):
    product = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    offer_id = models.CharField(max_length=100)
    purchased_product = models.IntegerField(null=True)
    purchased_product_warehouse = models.IntegerField(null=True)
    purchased_warehouse = models.IntegerField(null=True)
    proceeds_product = models.BigIntegerField(null=True)
    proceeds_product_warehouse = models.BigIntegerField(null=True)
    proceeds_warehouse = models.BigIntegerField(null=True)
    proceeds_product_percent = models.DecimalField(null=True, max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    proceeds_product_warehouse_percent = models.DecimalField(null=True, max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    proceeds_warehouse_percent = models.DecimalField(null=True, max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    abc_products = models.CharField(max_length=1)
    abc_product_warehouse = models.CharField(max_length=1)
    abc_warehouse = models.CharField(max_length=1)

    shop = models.IntegerField()
