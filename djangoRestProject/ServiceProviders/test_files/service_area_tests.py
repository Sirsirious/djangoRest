import pytest
from django.core.exceptions import ValidationError

from djangoRestProject.ServiceProviders.models import ServiceArea


def test_service_area_model(
    transactional_db, simple_polygon_geojson, simple_polygon_str, base_provider
):
    service_area = ServiceArea()
    service_area.name = "Test Service Area"
    service_area.price = 10.0
    service_area.area = simple_polygon_str
    service_area.area_json = simple_polygon_geojson
    service_area.provider = base_provider
    service_area.save()
    service_area.full_clean()


def test_service_area_model_missing_field(
    transactional_db, simple_polygon_geojson, simple_polygon_str, base_provider
):
    service_area = ServiceArea()
    service_area.name = ""
    service_area.price = 10.0
    service_area.area = simple_polygon_str
    service_area.area_json = simple_polygon_geojson
    service_area.provider = base_provider
    service_area.save()
    with pytest.raises(ValidationError):
        service_area.full_clean()


def test_service_area_model_invalid_price(
    transactional_db, simple_polygon_geojson, simple_polygon_str, base_provider
):
    service_area = ServiceArea()
    service_area.name = "Test Service Area"
    service_area.price = -10.0
    service_area.area = simple_polygon_str
    service_area.area_json = simple_polygon_geojson
    service_area.provider = base_provider
    service_area.save()
    with pytest.raises(ValidationError):
        service_area.full_clean()
