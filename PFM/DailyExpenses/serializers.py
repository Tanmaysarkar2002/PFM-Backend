from rest_framework import serializers
from DailyExpenses.models import ExpenseCategory


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['name' ,'user']
