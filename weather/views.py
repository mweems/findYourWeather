from django.shortcuts import render

def index(request):
	user = 'Matt Weems'
	return render(request, 'index.html', {'user': user})

def login(request):
	return render(request, 'login.html')
