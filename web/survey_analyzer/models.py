from django.db import models

# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(null=True, blank=True)
    timestamp = models.DateTimeField()
