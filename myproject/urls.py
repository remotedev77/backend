from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('app/', include('my_app.urls')),
    path('auth/', include('users.urls')),
    # path('admin-api/', include('admin_app.urls')),
    path('questions/', include('admin_app.urls.questions_urls')),
    path('answers/', include('admin_app.urls.answers_urls')),
    path('users/', include('admin_app.urls.users_urls')),
    path('companies/', include('admin_app.urls.companies_urls')),
    path('managers/', include('admin_app.urls.managers_urls')),
    path('directions/', include('admin_app.urls.directions_urls')),

]
admin.site.site_header = "Edu Simulator Admin"
admin.site.site_title = "Edu Simulator"
admin.site.index_title = "Welcome to Edu Simulator Admin"
admin.site.site_url="https://edu-simulator.ru/"
