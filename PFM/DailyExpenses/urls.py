from django.contrib import admin
from django.urls import path , include
from DailyExpenses.views import (AddDailyExpense, 
                                 GetAllExpenses,
                                 ListExpenseCategories,
                                 AddExpenseCategory,
                                 DeleteExpenseCategory)

admin.autodiscover()
app_name = 'DailyExpenses'


urlpatterns = [
    path('add-expense/', AddDailyExpense.as_view(), name='add_expense'),
    path('get-expenses/', GetAllExpenses.as_view(), name='get_expenses'),
    path('categories/', ListExpenseCategories.as_view(), name='list-categories'),
    path('add-category/', AddExpenseCategory.as_view(), name='add-category'),
    path('delete-category/<int:category_id>/', DeleteExpenseCategory.as_view(), name='delete-category'),
]