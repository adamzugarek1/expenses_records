from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('CZK', 'CZK'),
        ('GBP', 'GBP'),
    ])
    date = models.DateField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
