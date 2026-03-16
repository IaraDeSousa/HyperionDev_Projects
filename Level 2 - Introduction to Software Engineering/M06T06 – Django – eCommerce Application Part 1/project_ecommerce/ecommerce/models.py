from django.conf import settings
from django.db import models


class Store(models.Model):
    '''
    Model representing a store, which has a vendor and a name.
    '''
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)


class Product(models.Model):
    '''
    Model representing a product, which belongs to a store and has
    a name, price, and stock quantity.
    '''
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=1)


class ResetToken(models.Model):
    '''
    Model representing a password reset token, which is associated with
    a user and has a token value, expiry date, and determines if it has
    been used.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)


class Purchase(models.Model):
    '''
    Model representing a purchase, which is associated with a user
    and a product, and has a date of purchase.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_bought = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    '''
    Model representing a product review, which is associated with a
    user and a product, it also has content and a verification status.
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    is_verified = models.BooleanField(default=False)
