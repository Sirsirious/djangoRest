from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from djangoRestProject.ServiceProviders.models import Provider, ServiceArea


# Create your views here.
from rest_framework import viewsets
from djangoRestProject.ServiceProviders.serializers import (
    ProviderSerializer,
    ServiceAreaSerializer,
    ServiceAreaMatchInputSerializer,
    ServiceAreaMatchOutputSerializer,
)


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Providers to be viewed or edited.
    """

    queryset = Provider.objects.all().order_by("-name")
    serializer_class = ProviderSerializer
    permission_classes = []


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ServiceAreas to be viewed or edited.
    """

    queryset = ServiceArea.objects.all().order_by("-name")
    serializer_class = ServiceAreaSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save()


class ServiceAreaMatch(APIView):
    @swagger_auto_schema(
        request_body=ServiceAreaMatchInputSerializer,
        responses={200: ServiceAreaMatchOutputSerializer, 400: "Bad Request"},
    )
    def post(self, request, *args, **kwargs):
        """
        API endpoint that allows one to search for ServiceAreas that match a given point.
        """
        # Get the input data from serializer
        serializer = ServiceAreaMatchInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get the longitude and latitude - Be aware that GeoJSON uses longitude, latitude
        lng = serializer.validated_data.get("longitude")
        lat = serializer.validated_data.get("latitude")
        # Get the ServiceAreas that match the point - we use st_contains from postgis
        # We're using a GIST index to make this search faster
        # Other alternatives would be using creativity to create a custom index, like a map.
        # Due to the time constraint, I'm using the GIST index.
        sql_script = f"""SELECT *
                        FROM "ServiceProviders_servicearea" sa 
                        WHERE st_contains(sa.area, st_point({lat}, {lng}, 4326));"""
        # Execute the query
        cursor = connection.cursor()
        cursor.execute(sql_script)
        matched_areas = cursor.fetchall()
        if not matched_areas:
            # We return 404 if no ServiceArea is found, attempting to attain to REST principles
            return Response(
                status=404,
                data={
                    "message": f"No Service Area found for point of "
                    f"latitude {lat} and longitude {lng}."
                },
            )
        # As the GIST index is lossy, we need to filter the results to make sure we got real matches
        service_areas = ServiceArea.objects.filter(
            id__in=[area[0] for area in matched_areas]
        )
        # Serialize the results and return them
        return Response(ServiceAreaMatchOutputSerializer(service_areas, many=True).data)
