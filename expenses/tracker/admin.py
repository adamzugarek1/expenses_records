from django.contrib import admin

from .models import Category, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass