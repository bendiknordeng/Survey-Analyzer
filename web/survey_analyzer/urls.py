from django.urls import path
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('define_structure', views.define_structure, name='define_structure'),
    path('analyze', views.analyze, name='analyze'),
    path('jacobtest', views.jacobtest, name='jacobtest')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
