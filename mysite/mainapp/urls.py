# mainapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/latest/', views.latest_data, name='latest_data'),
    path('api/history/', views.history_data, name='history_data'),
    path('api/raw/', views.raw_data, name='raw_data'),
]