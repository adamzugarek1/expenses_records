# views.py
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .models import Category, Expense
from .forms import *


class ExpenseListView(View):
    template_name = 'tracker/expense_list.html'

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()
        categories = Category.objects.all()
        return render(request, self.template_name, {'expenses': expenses, 'categories': categories})


class AddExpenseView(View):
    template_name = 'tracker/add_expense.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = ExpenseForm(categories=categories)
        return render(request, self.template_name, {'categories': categories, 'form': form})

    def post(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = ExpenseForm(request.POST, categories=categories)

        if form.is_valid():
            category_id = form.cleaned_data['category'].id

            category = Category.objects.get(id=category_id)

            expense = form.save(commit=False)
            expense.category = category
            expense.user = request.user
            expense.save()

            form.save()

            return redirect('expense_list')

        return render(request, self.template_name, {'form': form})


class ManageCategoriesView(View):
    template_name = 'tracker/manage_categories.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, self.template_name, {'categories': categories, 'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manage_categories')

        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories, 'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('expense_list')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'tracker/login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'tracker/register.html', {'form': form})


class PasswordChangeView(View):
    template_name = 'tracker/password_change.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('expense_list')

        return render(request, self.template_name, {'form': form})
