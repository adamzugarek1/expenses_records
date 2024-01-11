from django.urls import path
from .views import *

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense_list'),
    path('add_expense/', AddExpenseView.as_view(), name='add_expense'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('manage_categories/', ManageCategoriesView.as_view(), name='manage_categories'),
]
