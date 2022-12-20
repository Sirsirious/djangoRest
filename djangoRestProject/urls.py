from django.urls import include, re_path
from django.urls import path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from djangoRestProject.ServiceProviders import views

schema_view = get_schema_view(
    openapi.Info(
        title="Django REST API",
        default_version="v1",
        description="An API by Tiago Duque",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tfduque@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r"provider", views.ProviderViewSet)
router.register(r"service-area", views.ServiceAreaViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^service-area-match/$", views.ServiceAreaMatch.as_view(), name="match"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
