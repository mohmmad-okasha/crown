from django.shortcuts import render,redirect
from users import models
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/users/login")
def index(request):
	return render(request,"dashboard.html",{'users':models.Users.objects.all().order_by('id')})

def test(request):
	return render(request,"test.html")

