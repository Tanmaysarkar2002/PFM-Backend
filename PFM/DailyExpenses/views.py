from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from DailyExpenses.models import DailyExpenses,ExpenseCategory
from DailyExpenses.serializers import ExpenseCategorySerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AddDailyExpense(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        amount = data.get('amount')
        date = data.get('date')
        description = data.get('description')
        category_name = data.get('category')
        user = request.user

        if not amount or not date or not description or not category_name:
            return Response({'error': 'Please provide all fields'}, status=status.HTTP_400_BAD_REQUEST)

        user_detail = User.objects.get(username=user)
        try:
            category = ExpenseCategory.objects.get(name=category_name, user=request.user)
        except ExpenseCategory.DoesNotExist:
            return Response({'error': 'Category not present to add expense. Add category first.'}, status=status.HTTP_400_BAD_REQUEST)

        expense = DailyExpenses.objects.create(
            user=user_detail,
            amount=amount,
            date=date,
            description=description,
            category=category
        )

        return Response({'message': 'Expense Added successfully'}, status=status.HTTP_200_OK)


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
                'id':expense.expense_id,
                'amount': expense.amount,
                'date': expense.date,
                'description': expense.description,
                'category': expense.category.name
            })

        return Response(data, status=status.HTTP_200_OK)

class RemoveExpense(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        expense_id = data.get('expense_id')
        user = request.user

        if not expense_id:
            return Response({'error': 'Please provide expense_id'}, status=status.HTTP_400_BAD_REQUEST)

        user_detail = User.objects.get(username=user)
        try:
            expense = DailyExpenses.objects.get(user=user_detail, id=expense_id)
        except DailyExpenses.DoesNotExist:
            return Response({'error': 'No such expense found'}, status=status.HTTP_400_BAD_REQUEST)

        expense.delete()
        return Response({'message': 'Expense removed successfully'}, status=status.HTTP_200_OK)
    
class ListExpenseCategories(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = ExpenseCategory.objects.all()
        category_data = [{"id": category.id, "name": category.name} for category in categories]
        return Response(category_data, status=status.HTTP_200_OK)


class AddExpenseCategory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        if ExpenseCategory.objects.filter(name=name).exists():
            return Response({"detail": "Category with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['user'] = request.user.id
        serializer = ExpenseCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Category Added Successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteExpenseCategory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id):
        try:
            category = ExpenseCategory.objects.get(id=category_id)
            category.delete()
            return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ExpenseCategory.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)