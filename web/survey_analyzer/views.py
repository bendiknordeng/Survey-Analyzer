from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files import File
from django.conf import settings
from .source.file_converter import Converter

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['survey']
        file_storage = FileSystemStorage()
        path = file_storage.save(uploaded_file.name, uploaded_file)
        paths = Converter(settings.MEDIA_ROOT+path).save(settings.MEDIA_ROOT)
        default_storage.delete(path)
    return render(request, 'home.html')

def define_structure(request):
    return render(request, 'define_structure.html')

def analyze(request):
    return render(request, 'analyze.html')
