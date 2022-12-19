from django.contrib.gis.db import models as geo_models
from django.core.validators import MinValueValidator, validate_email
from django.db import models


class Provider(models.Model):
    """
    Provider model - stores all service providers
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(
        max_length=100, validators=[validate_email], null=False, blank=False
    )
    phone_number = models.CharField(max_length=20, null=False)
    language = models.CharField(max_length=10, default="en")
    currency = models.CharField(max_length=10, default="USD")


class ServiceArea(models.Model):
    """
    ServiceArea model - stores all service areas
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    area = geo_models.PolygonField()
    area_json = models.JSONField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
