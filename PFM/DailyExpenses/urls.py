from django.contrib import admin
from django.urls import path , include
from DailyExpenses.views import AddDailyExpense, GetAllExpenses

admin.autodiscover()
app_name = 'DailyExpenses'


urlpatterns = [
    path('add-expense/', AddDailyExpense.as_view(), name='add_expense'),
    path('get-expenses/', GetAllExpenses.as_view(), name='get_expenses')
]