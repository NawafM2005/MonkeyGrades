from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name= 'signup'),
    path('signin', views.signin, name= 'signin'),
    path('signout', views.signout, name= 'signout'),
    path('dashboard', views.dashboard, name= 'dashboard'),
    path('simple', views.simple, name= 'simple'),
    path('remove_course', views.remove_course, name= 'remove_course'),
    path('add_course', views.add_course, name= 'add_course'),
]