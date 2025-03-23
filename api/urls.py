from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication


schema_view = get_schema_view(
    openapi.Info(
        title="Ricopin Wishlist API",
        default_version="v1",
        description="API documentation for the Wishlist project with JWT-based authentication",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user_auth.urls")),
    path("api/", include("wishlist.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("", include("django_prometheus.urls")),
]
