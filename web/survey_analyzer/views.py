from django.shortcuts import render
from .source.file_converter import Converter
from .models import Survey


def home(request):
    context = {}
    return render(request, 'home.html', context)

def analyze(request):
    file = Survey(request.POST)
    print(file)
    return render(request, 'analyze.html')
