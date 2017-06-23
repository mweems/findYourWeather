import requests
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	user = 'Matt Weems'
	if request.method == 'POST':
		city = request.POST.get('city')
		response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + '&mode=json&units=imperial&APPID=9f592b7a51c96031cae6cb887d0594c4')
		data = response.json()
		print(data)
		today = {'city': data['name'], 'temp': data['main']['temp'], 'temp_max': data['main']['temp_max'],
				'temp_min': data['main']['temp_min'], 'description': data['weather'][0]['description']}
		return render(request, 'index.html', {'user': user, 'today': today})
	return render(request, 'index.html', {'user': user})

def login(request):
	return render(request, 'login.html')
