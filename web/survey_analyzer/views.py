from django.shortcuts import render
from .source.file_converter import Converter
from tkinter import filedialog
from .models import Survey
import numpy as np


def home(request):
    dialog = filedialog
    return render(request, 'home.html')

def analyze(request):
    survey = Survey(request.POST)
    img = Converter(survey.file)
    return render(request, 'analyze.html')
