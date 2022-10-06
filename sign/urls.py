from django.urls import path

from .views import remote_sign

app_name = 'sign'
urlpatterns = [
    path('', remote_sign.index, name='index')
]
