from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.initials, name='initial'),
    path('payload/', views.handle_payload, name='payload'),

]

