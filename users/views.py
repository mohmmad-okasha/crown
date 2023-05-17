from django.shortcuts import render,redirect
from . import models,forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/users/login")
def index(request):
	form= forms.users_form
	# user_name= request.POST.get('user_name')
	# user_email= request.POST.get('email')
	# data =Users(name=user_name,email=user_email)
	# data.save()
	message = 'from view'
	
	return render(request,"users/index.html",{'message2':message,'u_id':-1,'form':form ,'users':models.Users.objects.all().order_by('id')})

@login_required(login_url="/users/login")
def add(request):
	form = forms.users_form()
	if request.method == "POST":
		form = forms.users_form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('users:index')
	return render(request,'users/add.html',{'form': form})


def delete(request,row_id):
	print(row_id)
	if row_id is not None :
		models.Users.objects.get(id=row_id).delete()
	return redirect('users:index')

def update_user(request,row_id):
	if row_id is not None :
		models.Users.objects.get(id=row_id).delete()
	return redirect('users:index')


def login_view(request):
	if request.method == "POST":
		form =AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST: # if the login will redirect to a page
				return redirect(request.POST.get('next'))
			else:
				return redirect('users:index')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form': form})

# def login_view(request):
# 	if request.method == "POST":
# 		form =forms.Login_form(data=request.POST)
		
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		user = authenticate(request, username=username, password=password)

# 		if user is not None:
# 			login(request,user)
# 			if 'next' in request.POST: # if the login will redirect to a page
# 				return redirect(request.POST.get('next'))
# 			else:
# 				return redirect('users:index')
# 		else:
# 			print('error login')
# 	else:
# 		form = forms.Login_form()
# 	return render(request,'login.html',{'form': form})

def logout_view(request):
	if request.method == "POST":
		logout(request)
		return redirect('users:login')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form': form})

@login_required(login_url="/users/login")
def about(request):
	return render(request,"about.html",{'user_name':request.user})


def signup(request):
	form = UserCreationForm()
	return render(request,'test.html',{'form' : form})

