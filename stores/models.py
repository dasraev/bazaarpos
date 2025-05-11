from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=255,blank=True,default="")
    image = models.ImageField(null=True,blank=True,upload_to='stores/')