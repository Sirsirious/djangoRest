import json

import pytest


def test_create_provider_end_to_end(client, base_provider):
    response = client.post(
        "/provider/",
        {
            "name": "Test Provider",
            "email": "email@test.com",
            "phone_number": "123456789",
            "language": "en",
            "currency": "USD",
        },
        format="json",
    )
    assert response.status_code == 201


def test_create_service_area_end_to_end(client, base_provider, simple_polygon_geojson):
    response = client.post(
        "/service-area/",
        {
            "name": "Test Service Area",
            "price": 100.0,
            "area_json": json.dumps(simple_polygon_geojson),
            "provider": base_provider.id,
        },
        format="json",
    )
    assert response.status_code == 201


@pytest.mark.parametrize(
    "lat,lng,expected",
    [
        (30.0, 15.0, 1),
        (35.0, 15.0, 0),
    ],
)
def test_check_point_within_area(client, base_service_area, lat, lng, expected):
    response = client.post(
        "/service-area-match/",
        {
            "latitude": lat,
            "longitude": lng,
        },
    )
    if expected == 1:
        assert response.status_code == 200
        assert "name" in response.data[0]
        assert "price" in response.data[0]
        assert "provider" in response.data[0]
    else:
        assert response.status_code == 404
