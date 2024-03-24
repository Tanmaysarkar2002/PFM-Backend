from django.db import models

class UserInformation(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField()
    address = models.CharField(max_length=500)
    account_location = models.CharField(max_length=200)