from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
	print "Debug"
	return render(request, "app1/index.html")