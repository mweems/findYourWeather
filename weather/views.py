import requests
import json
import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	user = 'Matt Weems'
	if request.method == 'POST':
		city = request.POST.get('city')
		daily = getDailyForecast(city)
		forecast = getWeeklyForecast(city)
		
		today = {'city': daily['name'], 'temp': int(daily['main']['temp']),
				 'temp_max': int(daily['main']['temp_max']),'temp_min': int(daily['main']['temp_min']),
				  'description': daily['weather'][0]['main']}
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
		return render(request, 'index.html', {
			'user': user, 
			'today': today, 
			'forecast': forecast_list})
	return render(request, 'index.html', {'user': user})

def login(request):
	return render(request, 'login.html')

def getDailyForecast(city):
	daily = requests.get("http://api.openweathermap.org/data/2.5/weather?q="
		 	+ city + '&mode=json&units=imperial&APPID=9f592b7a51c96031cae6cb887d0594c4')
	return daily.json()

def getWeeklyForecast(city):
	forecast = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" 
			+ city + '&mode=json&units=imperial&APPID=9f592b7a51c96031cae6cb887d0594c4')
	return forecast.json()
