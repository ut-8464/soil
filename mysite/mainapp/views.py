# mainapp/views.py
from django.shortcuts import render
from django.utils import timezone


def home(request):
    current_time = timezone.localtime()
    return render(request, 'mainapp/index.html', {
        'current_time': current_time,
    })