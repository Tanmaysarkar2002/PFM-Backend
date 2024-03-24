from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DailyExpenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.user.user.username