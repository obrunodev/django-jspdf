from django.urls import path

from perguntas import views

app_name = 'perguntas'
urlpatterns = [
    path('', views.perguntas_list, name='list'),
    path('create/', views.perguntas_create, name='create'),
]
