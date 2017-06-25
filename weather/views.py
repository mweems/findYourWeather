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
		if 'change_current' in request.POST:
			cy = City.objects.get(user=user)
			cy.current_city = city
			cy.save()
		fetch = True		
	if fetch:
		data = renderWeather(request, city)
		data['user'] = user
		data['date'] = date
		return render(request, 'index.html', data)

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

	return {'today': daily, 'forecast': forecast}

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
		time_map = {'00:00:00': 'Midnight', '03:00:00': '3 AM', '06:00:00': '6 AM',
					'09:00:00': '9 AM', '12:00:00': 'Noon', '15:00:00': '3 PM',
					'18:00:00': '6 PM', '21:00:00': '9 PM'}
		for data in forecast.get('list'):
			time = str(data['dt_txt'][11:])
			rep = {
				'date': datetime.datetime.strptime(data['dt_txt'][:10], '%Y-%m-%d').date(),
				'time': time_map.get(time),
				'temp': data['main']['temp'],
				'temp_max': int(data['main']['temp_max']),
				'temp_min': int(data['main']['temp_min']),
				'description': data['weather'][0]['description'],
				'main': data['weather'][0]['main']
			}
			forecast_list.append(rep)
		forecast_list = getWeeklyAvgList(forecast_list)
	except:
		forecast_list = {'error': True}
	return forecast_list

def getWeeklyAvgList(forecast_list):
	week = []
	day = []
	date = ''
	for item in forecast_list:
		ldate = item['date']
		if not date:
			date = item['date']
		if ldate == date:
			day.append(item)
		else:
			week.append(day)
			day = []
			day.append(item)
			date = item['date']
	return week




