from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import CityWeather, Users
from django.conf import settings


# Create your views here.


def index(request):
    return render(request, 'weather.html')


def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')


@csrf_exempt
def getWeather(request):
    print("Weather")
    city = request.GET.get("city")
    
    print("City-", city)
    weather = []

    url = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=' + settings.API_KEY+ '&q='+ city
    r = requests.get(url).json()
    if r == []:
        weather_dict = {
            'temp': '0° F',
            'icon': '',
            'description': '',
            'city':'No Details Available'
        }
    else:    
        print('key-', r)
        for data in r:
            key = data['Key']
        
        print(key)
        url = 'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/'+ key +'?apikey=' + settings.API_KEY
        r = requests.get(url).json()
        print('weather details-', r)
        
        for data in r:
            temperature = str(data['Temperature']['Value']) + '° F'
            icon = data['WeatherIcon']
            description = data['IconPhrase']
            weather_dict = {
                'temp': temperature,
                'icon': icon,
                'description': description,
                'city': city
            }
            weather_instance = CityWeather.objects.create(city=city, temperature=temperature, description=description, icon=icon)
            weather_instance.save() 
    weather.append(weather_dict)
    response_data = {"weather": weather}
    print(response_data)
    return JsonResponse(response_data)


def auth(request):
    name = request.POST['name']
    username = request.POST['username']
    pswd = request.POST['pswd']
    cnf_pswd = request.POST['cnf_pswd']

    if pswd == cnf_pswd:
        if Users.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!!!")
            return redirect('signup')
        else:
            try:
                validate_email(username)
            except ValidationError as e:
                messages.info(request, "Enter valid Email Address!!!")
                return redirect('signup')

            user_instance = Users.objects.create(name=name, username=username, pswd=pswd, type="")
            user_instance.save()
            messages.info(request, "Congratulations!!!Your account has been created.")
            return redirect('login')
    else:
        messages.info(request, "Passwords not matching!!!")
        return redirect('signup')

def logging(request):
    print("Login submit")
    if request.GET.get('signin') == 'signin':
        return redirect('login')
    else:
        username = request.POST['uname']
        pswd = request.POST['psw']

        try:
            p = Users.objects.get(username=username, pswd=pswd)
            if p is not None:

                return redirect('index')
        except Users.DoesNotExist:
            messages.info(request, "Incorrect Username or Password!!!")
            return redirect('login')





 

