from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
	print "Debug"
	if 'user' in request.session:
		return redirect('/home')
	return render(request, "app1/login.html")

def register(request):
	if request.method == "POST":
		result = User.objects.register(request.POST)
		if result['registered']:
			request.session['user'] = result['newUser'].first_name
			return redirect('/home')
		else:
			for error in result['errors']:
				messages.add_message(request, messages.ERROR, error)


		return redirect('/')

def login(request):
	if request.method == "POST":
		loginResult = User.objects.validateLogin(request.POST)

		if not loginResult:
			messages.add_message(request, messages.ERROR, "invalid email/password combination.")
			return redirect('/')

		else:
			request.session['user'] = {
			'id': loginResult.id,
			'first_name': loginResult.first_name,
			'last_name': loginResult.last_name,
			'email': loginResult.email
			}
			return redirect('/home')	

	else:
		return redirect('/')

def home(request):

	return render(request, 'app1/index.html')

def logout(request):
	if request.method == "POST":
		request.session.pop('user')
		return redirect('/')
	else:
		return redirect('/')


