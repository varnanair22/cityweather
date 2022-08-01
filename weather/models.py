from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    pswd = models.CharField(max_length= 100)
    type = models.CharField(max_length = 50)
    
    
class CityWeather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.CharField(max_length=100)
    description = models.CharField(max_length= 100)
    icon = models.CharField(max_length = 50)
