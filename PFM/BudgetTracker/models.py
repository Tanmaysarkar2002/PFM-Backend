from django.db import models
from django.contrib.auth.models import User
from DailyExpenses.models import ExpenseCategory
from django.utils import timezone
from BudgetTracker.tasks import send_notification_email
from decimal import Decimal
from datetime import date


class Budget(models.Model):
    category = models.OneToOneField(ExpenseCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.category.name}: {self.amount}'

class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.name} - {self.goal_amount}'

    def check_and_send_notifications(self):
        today = timezone.now().date()  # Get the current date
        if self.current_amount >= Decimal(0.9) * self.goal_amount:
            print("Calling send_notification_email")
            send_notification_email.delay(
                'You are close to achieving your saving goal',
                'You have saved 90% of your goal amount. Keep going!',
                'sarkartanmay646@gmail.com',
                [self.user.email],
            )
        elif self.current_amount < self.goal_amount * Decimal((today - self.created_at.date()).days) / Decimal((self.goal_date - self.created_at.date()).days):
            print("Calling send_notification_email")
            send_notification_email.delay(
                'You are falling behind on your saving goal',
                'You are not saving enough to achieve your goal by the target date. Please consider saving more.',
                'sarkartanmay646@gmail.com',
                [self.user.email],
            )

    def deposit(self, amount):
        amount = Decimal(amount) 
        if amount > 0:
            self.current_amount += amount
            self.save()

    def withdraw(self, amount):
        amount = Decimal(amount) 
        if amount > 0 and amount <= self.current_amount:
            self.current_amount -= amount
            self.save()

    def is_completed(self):

        return self.current_amount >= self.goal_amount and not self.completed

    def mark_as_completed(self):

        if self.is_completed():
            self.completed = True
            self.save()

class Transaction(models.Model):
    DEPOSIT = 'D'
    WITHDRAWAL = 'W'
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    saving_goal = models.ForeignKey(SavingGoal, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(default=timezone.now)