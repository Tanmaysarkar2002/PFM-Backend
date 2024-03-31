from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Sum
from BudgetTracker.models import Budget ,SavingGoal,Transaction
from DailyExpenses.models import DailyExpenses,ExpenseCategory
from BudgetTracker.serializers import SavingGoalSerializer,TransactionSerializer
from decimal import Decimal



class SetBudget(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, category_id):
        amount = request.data.get('amount')
        try:
            category = ExpenseCategory.objects.get(id=category_id, user=request.user)
        except ExpenseCategory.DoesNotExist:
            return Response({'error': 'Category not present. Add category first.'}, status=status.HTTP_400_BAD_REQUEST)
        
        Budget.objects.update_or_create(category=category, user=request.user, defaults={'amount': amount})
        return Response({"detail": "Budget set successfully."}, status=status.HTTP_200_OK)


class GetBudgets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = ExpenseCategory.objects.filter(user=request.user)
        data = []
        for category in categories:
            total_spent = DailyExpenses.objects.filter(category=category, user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
            total_spent = Decimal(total_spent)
            try:
                budget = Budget.objects.get(category=category, user=request.user)
                remaining = budget.amount - total_spent
                budget_amount = str(budget.amount)
            except Budget.DoesNotExist:
                remaining = 'No budget set'
                budget_amount = 'No budget set'
            data.append({
                'category': category.name,
                'budget': budget_amount,
                'total_spent': str(total_spent),
                'remaining': remaining
            })
        return Response(data, status=status.HTTP_200_OK)
    

class SavingGoalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SavingGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'Message': 'Goal Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, goal_id=None):
        if goal_id is not None:
            try:
                goal = SavingGoal.objects.get(id=goal_id, user=request.user)
                serializer = SavingGoalSerializer(goal)
            except SavingGoal.DoesNotExist:
                return Response({'error': 'Saving goal not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            goals = SavingGoal.objects.filter(user=request.user)
            serializer = SavingGoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, goal_id):
        try:
            goal = SavingGoal.objects.get(id=goal_id, user=request.user)
        except SavingGoal.DoesNotExist:
            return Response({'error': 'Goal not present.'}, status=status.HTTP_400_BAD_REQUEST)

        amount = request.data.get('amount')
        action = request.data.get('action')

        if action in ['increase_goal', 'deposit', 'withdraw'] and amount is None:
            return Response({'error': 'Amount is required for this action.'}, status=status.HTTP_400_BAD_REQUEST)

        if action is None:
            return Response({'error': 'Action is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'increase_goal':
            if amount is not None:
                goal.goal_amount += amount
            else:
                return Response({'error': 'Amount is required to increase goal.'}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'deposit':
            # Create the transaction
            transaction = Transaction(
                saving_goal=goal,
                amount=amount,
                transaction_type=Transaction.DEPOSIT,
            )
            transaction.save()

            # Update the saving goal
            goal.goal_amount += amount
        elif action == 'withdraw':
            # Check if there are sufficient funds
            if goal.amount < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the transaction
            transaction = Transaction(
                saving_goal=goal,
                amount=amount,
                transaction_type=Transaction.WITHDRAWAL,
            )
            transaction.save()

            # Update the saving goal
            goal.amount -= amount
        elif action == 'mark_as_completed':
            goal.mark_as_completed()
        else:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        goal.save()
        return Response({'message': 'Action performed successfully'}, status=status.HTTP_200_OK)


class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        saving_goal_id = self.kwargs['saving_goal_id']
        return Transaction.objects.filter(saving_goal__id=saving_goal_id)