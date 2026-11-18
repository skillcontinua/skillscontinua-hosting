# File path: C:\hosting\skillscontinua_hosting\core\urls.py
from django.urls import path
from .views import home_view

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
]