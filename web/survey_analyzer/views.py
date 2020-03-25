from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files import File
from django.conf import settings
from .source.file_converter import Converter

def home(request):
    return render(request, 'home.html')

def define_structure(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['survey']
        file_storage = FileSystemStorage()
        path = file_storage.save(uploaded_file.name, uploaded_file)
        file = default_storage.open(path).read()
        paths = Converter(file, uploaded_file.name).save(settings.MEDIA_ROOT)
        default_storage.delete(path)
        context['path'] = paths[0]
    return render(request, 'define_structure.html', context)

def analyze(request):
    return render(request, 'analyze.html')
    
def jacobtest(request):
    dialog = filedialog
    return render(request, 'jacobtest.html')

