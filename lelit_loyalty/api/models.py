from django.db import models


class User(models.Model):
    user_id = models.IntegerField()
    lang = models.CharField(max_length=2, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    barcode = models.CharField(max_length=9, null=True, blank=True)
    birth_date = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    balance = models.IntegerField()


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sum = models.IntegerField()
    type = models.CharField(max_length=5)
    datetime = models.IntegerField()