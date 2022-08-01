from django.urls import path
from . import views

urlpatterns = [
#   path('', views.index),
  path('', views.login),
  path('login/', views.login, name="login"),
  path('signup', views.signup, name="signup"),
  path('auth', views.auth, name="auth"),
  path('logging', views.logging, name="logging"),
  path('login/logging', views.logging, name="logging"),
  path('login/signup', views.signup, name="signup"),
  path('login/auth', views.auth, name="auth"),
  path('get_weather/', views.getWeather, name="weather"), 
  path('weather', views.index, name="index"),
]
