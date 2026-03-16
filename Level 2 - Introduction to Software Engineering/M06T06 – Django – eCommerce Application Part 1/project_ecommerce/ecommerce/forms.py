from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Store, Product


class RegistrationForm(UserCreationForm):
    ''' Form for user registration. '''
    email = forms.EmailField(required=True)
    ACCOUNT_TYPE_CHOICES = (
        ("vendor", "Vendor"),
        ("buyer", "Buyer"),
    )
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES, required=True
    )

    class Meta:
        ''' Meta class for RegistrationForm, includes username, email,
        password, and account type fields. '''
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "account_type",
        ]


class StoreForm(forms.ModelForm):
    ''' Form for creating and editing stores. '''
    class Meta:
        ''' Meta class for StoreForm, includes name field. '''
        model = Store
        fields = ["name"]


class ProductForm(forms.ModelForm):
    ''' Form for creating and editing products. '''
    class Meta:
        ''' Meta class for ProductForm, includes name, price, and
        stock fields. '''
        model = Product
        fields = ["name", "price", "stock"]
