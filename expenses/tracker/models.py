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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class ExchangeRate(models.Model):
    currency = models.CharField(max_length=3, choices=[
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    ])  # Currency code (e.g., USD, EUR, CZK)
    rate = models.DecimalField(max_digits=10, decimal_places=3)  # Exchange rate relative to CZK
    date = models.DateField()

    def __str__(self):
        return f"1 {self.currency} = {self.rate} CZK"

    class Meta:
        unique_together = ['date', 'currency']
