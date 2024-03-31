from rest_framework import serializers
from BudgetTracker.models import SavingGoal,Transaction

class SavingGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingGoal
        fields = ['id', 'user', 'name', 'goal_amount', 'current_amount', 'goal_date', 'completed', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'required': False}}


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'