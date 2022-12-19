import pytest

from djangoRestProject.ServiceProviders.models import Provider, ServiceArea


@pytest.fixture()
def base_provider(transactional_db):
    provider = Provider()
    provider.name = "Test Provider"
    provider.email = "provider@test.com"
    provider.phone_number = "123456789"
    provider.language = "en"
    provider.currency = "US"
    provider.save()
    return provider


@pytest.fixture()
def simple_polygon_geojson():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [30.0, 10.0],
                            [40.0, 40.0],
                            [20.0, 40.0],
                            [10.0, 20.0],
                            [30.0, 10.0],
                        ]
                    ],
                },
            }
        ],
    }


@pytest.fixture()
def simple_polygon_str(simple_polygon_geojson):
    POLYGON = "POLYGON(("
    for coords in simple_polygon_geojson["features"][0]["geometry"]["coordinates"][0]:
        POLYGON += f"{coords[0]} {coords[1]},"
    POLYGON = POLYGON[:-1] + "))"
    return POLYGON


@pytest.fixture()
def base_service_area(
    transactional_db, base_provider, simple_polygon_geojson, simple_polygon_str
):
    service_area = ServiceArea()
    service_area.name = "Test Service Area"
    service_area.price = 10.0
    service_area.area = simple_polygon_str
    service_area.area_json = simple_polygon_geojson
    service_area.provider = base_provider
    service_area.save()
    return service_area
