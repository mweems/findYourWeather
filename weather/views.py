import requests
import json
import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from weather.forms import SignUpForm
from weather.models import City

@csrf_exempt
def index(request):
	user = ''
	date = datetime.datetime.now()
	fetch = False

	if request.user.is_authenticated():
		user = User.objects.get(username=request.user.username)
	if request.user.is_authenticated() and not request.method == 'POST':
		city = user.city.current_city
		fetch = True
	if request.method == 'POST':
		city = request.POST.get('city')
		fetch = True		
	if fetch:
		forecast = renderWeather(request, city)
		forecast['user'] = user
		forecast['date'] = date
		return render(request, 'index.html', forecast)

	return render(request, 'index.html')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			city = City(user=user, current_city=form.cleaned_data.get('current_city'))
			city.save()
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

def renderWeather(request, city):
	daily = getDailyForecast(city)
	forecast = getWeeklyForecast(city)

	return { 'today': daily, 'forecast': forecast}

def getDailyForecast(city):
	try:
		daily = requests.get("http://api.openweathermap.org/data/2.5/weather?q="
			 	+ city + '&mode=json&units=imperial&APPID=9f592b7a51c96031cae6cb887d0594c4')
		daily = daily.json()
		today = {'city': daily['name'], 'temp': int(daily['main']['temp']),
					'temp_max': int(daily['main']['temp_max']),'temp_min': int(daily['main']['temp_min']),
					'description': daily['weather'][0]['main']}
	except:
		today = {'error': 'The City ' + city + ' could not be found. Please check the spelling and try again'}
	return today

def getWeeklyForecast(city):
	try:
		forecast = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" 
				+ city + '&mode=json&units=imperial&APPID=9f592b7a51c96031cae6cb887d0594c4')
		forecast = forecast.json()
		forecast_list = []
		for data in forecast['list']:
			rep = {
				'date': datetime.datetime.strptime(data['dt_txt'][:10], '%Y-%m-%d').date(),
				'temp': data['main']['temp'],
				'temp_max': data['main']['temp_max'],
				'temp_min': data['main']['temp_min'],
				'description': data['weather'][0]['description'],
				'main': data['weather'][0]['main']
			}
			forecast_list.append(rep)
	except:
		forecast_list = {'error': True}
	return forecast_list
