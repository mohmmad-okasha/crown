from django import forms
from . import models
from django.forms import ModelForm,widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# class Login_form(forms.ModelForm):
#     class Meta:
#         model = User # table
#         fields = ['username','password']   # OR fields = ['id','name',....]
#         widgets ={
#             'username':forms.TextInput(attrs={'class':'form-control'}),
#             'password':forms.PasswordInput(attrs={'class':'form-control'})
#         }
#         labels = {
#             'username': '',
#             'password': '',
#         }

class users_form(forms.ModelForm):
    class Meta:
        model= models.Users
        fields = '__all__'

class Test_form(forms.ModelForm):
    class Meta:
        model = models.Test_model # table
        fields = '__all__'   # OR fields = ['id','name',....]