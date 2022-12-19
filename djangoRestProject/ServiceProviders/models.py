from django.db import models
from django.contrib.gis.db import models as geo_models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)


class ServiceArea(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    area = geo_models.PolygonField()
    area_json = models.JSONField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
