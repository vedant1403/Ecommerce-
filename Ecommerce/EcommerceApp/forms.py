from EcommerceApp.models import Product
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django .forms import ModelForm
from .models import Product

class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields =['username','email','password1','password2']

class AddProduct(ModelForm):
    class Meta:
        model=Product
        fields="__all__"
