from django.urls import path

from . import views

#não tive necessidade de criar o caminho admin, não usei models
urlpatterns = [
    path('', views.index, name='index'),
    path('resultado', views.index2, name='index2')
]

