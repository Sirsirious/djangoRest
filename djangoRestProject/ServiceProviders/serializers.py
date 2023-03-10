from django.contrib.gis.geos import Polygon

from djangoRestProject.ServiceProviders.models import Provider, ServiceArea
from rest_framework import serializers


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("name", "email", "phone_number", "language", "currency")


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ("name", "price", "provider", "area_json")

    def save(self, *args, **kwargs):
        """Overriding the save method to convert the area_json to a Polygon"""
        # Get geojson from serializer
        geojson = self.validated_data.get("area_json")
        # Get the polygon coordinates
        features_list = geojson.get("features")
        has_polygon = [
            True
            for feature in features_list
            if feature.get("geometry", {}).get("type") == "Polygon"
        ]
        if not any(has_polygon):
            raise serializers.ValidationError(
                "The GEOJson must contain at least a polygon."
            )
        # Get the first polygon
        first_polygon = has_polygon.index(True)
        coordinates_list = features_list[first_polygon]["geometry"]["coordinates"]
        if coordinates_list:
            # Create a polygon object from the coordinates
            polygon = Polygon(*coordinates_list)
            # Set the polygon to the area field
            self.validated_data["area"] = polygon
            # Save the object to the database - it will be saved as a GIS field
            super().save(*args, **kwargs)
        else:
            raise serializers.ValidationError(
                "Invalid GeoJSON, the coordinates are empty."
            )


class ServiceAreaMatchInputSerializer(serializers.Serializer):
    """
    Serializer for the input of the ServiceAreaMatch API
    """

    longitude = serializers.FloatField()
    latitude = serializers.FloatField()


class ServiceAreaMatchOutputSerializer(serializers.Serializer):
    """
    Serializer for the output of the ServiceAreaMatch API.
    """

    name = serializers.CharField()
    price = serializers.CharField()
    provider = ProviderSerializer()
