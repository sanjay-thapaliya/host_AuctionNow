from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Product(models.Model):
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=32)
    product_detail = models.TextField(max_length=1000, null=True, blank=True)
    product_image = models.ImageField(upload_to='document/', max_length=254)
    product_price = models.CharField(max_length=32, default=1)
    date = models.DateTimeField(null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class BidDetail(models.Model):
    bid_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid_price = models.CharField(max_length=32)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bid_price
