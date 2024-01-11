from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense


from django import forms
from .models import Expense

from django import forms
from .models import Expense, Category

from django import forms
from .models import Expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category',  'amount', 'currency', 'date', 'name']

    def __init__(self, *args, categories=None, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        if categories:
            self.fields['category'].queryset = categories

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        # Ensure that either a pre-existing category or a custom category is provided
        if not category:
            raise forms.ValidationError('Please choose a category or enter a custom category.')

        # If a custom category is provided, set the category field to None

        return cleaned_data


class RegisterUser(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

