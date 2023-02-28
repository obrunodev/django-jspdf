from django.urls import path
from jspdf import views

app_name = 'jspdf'
urlpatterns = [
    path('', views.index, name='index'),
    path('send_pdf', views.send_pdf, name='send_pdf'),
]
