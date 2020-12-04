from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('roomsearch/', views.roomsearch, name='roomsearch'),
    path('applypromo/', views.applypromo, name='applypromo'),
]
