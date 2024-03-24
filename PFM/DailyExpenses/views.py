import copy
from django.shortcuts import render
from django.http import HttpResponse , JsonResponse

from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from DailyExpenses.models import DailyExpenses
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db import transaction



class AddDailyExpense(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        amount = data.get('amount')
        date = data.get('date')
        description = data.get('description')
        category = data.get('category')
        user = request.user

        if not amount or not date or not description or not category:
            return Response({'error': 'Please provide all fields'}, status=HTTP_400_BAD_REQUEST)

        user_detail = User.objects.get(username=user)
        expense = DailyExpenses.objects.create(
            user=user_detail,
            amount=amount,
            date=date,
            description=description,
            category=category
        )

        return Response({'message': 'Expense Added successfully'}, status=HTTP_200_OK)


class GetAllExpenses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_detail = User.objects.get(username=user)
        expenses = DailyExpenses.objects.filter(user=user_detail)
        data = []
        for expense in expenses:
            data.append({
                'amount': expense.amount,
                'date': expense.date,
                'description': expense.description,
                'category': expense.category
            })

        return Response(data, status=HTTP_200_OK)

class RemoveExpense(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        expense_id = data.get('expense_id')
        user = request.user

        if not expense_id:
            return Response({'error': 'Please provide expense_id'}, status=HTTP_400_BAD_REQUEST)

        user_detail = User.objects.get(username=user)
        try:
            expense = DailyExpenses.objects.get(user=user_detail, id=expense_id)
        except DailyExpenses.DoesNotExist:
            return Response({'error': 'No such expense found'}, status=HTTP_400_BAD_REQUEST)

        expense.delete()
        return Response({'message': 'Expense removed successfully'}, status=HTTP_200_OK)