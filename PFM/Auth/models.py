from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dob = models.DateField(max_length=200 , null=True , blank=True)
    address = models.CharField(max_length=500 , null=True , blank=True)
    account_location = models.CharField(max_length=200)
    phone = models.CharField(max_length=10, blank=True , null=True ,validators=[
                                RegexValidator(r'^\d{1,10}$')])

    def __str__(self):
        return self.user.username

