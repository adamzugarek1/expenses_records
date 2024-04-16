# views.py
import csv
from datetime import date

import requests
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .models import Category, Expense, ExchangeRate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum


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
            expense.user_id = request.user
            expense.save()

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


def expense_list(request):
    rates = ExchangeRate.objects.filter(date=date.today())

    if not rates:
        url = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt'

        page = requests.get(url)
        reader = csv.reader(page.text.split("\n"), delimiter="|")

        for row in reader:
            if len(row) == 5 and row[3] in ("GBP", "USD", "EUR"):
                ExchangeRate.objects.get_or_create(
                    currency=row[3],
                    date=date.today(),
                    rate=float(row[4].replace(",", ".")),
                )
        rates = ExchangeRate.objects.filter(date=date.today())

    exchange_rates = {"CZK": 1}

    for rate in rates:
       exchange_rates[rate.currency] = rate.rate

    expenses = Expense.objects.filter(user_id=request.user.id)
    sum_amount = 0

    for expense in expenses:
        expense.to_czk = expense.amount * exchange_rates[expense.currency]
        sum_amount += expense.to_czk

    context = {'rates': rates, "expenses": expenses, 'sum_amount': sum_amount}
    return render(request, 'tracker/expense_list.html', context)

