from django.urls import path
from .views import SetBudget, GetBudgets,SavingGoalView,TransactionView

urlpatterns = [
    path('set_budget/<int:category_id>/', SetBudget.as_view(), name='set_budget'),
    path('get_budgets/', GetBudgets.as_view(), name='get_budgets'),
    path('saving_goals/', SavingGoalView.as_view(), name='saving_goals'),
    path('saving_goals/<int:goal_id>/', SavingGoalView.as_view(), name='saving_goal_detail'),
    path('saving_goals/<int:saving_goal_id>/transactions/', TransactionView.as_view(), name='transactions'),
]