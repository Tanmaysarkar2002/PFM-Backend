import uuid
from django.db import models
from django.contrib.auth.models import User



class ExpenseCategory(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DailyExpenses(models.Model):
    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    description = models.CharField(max_length=200)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username
    
