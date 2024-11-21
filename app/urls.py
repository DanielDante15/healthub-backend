from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from django.urls import include, path,re_path
from django.conf.urls.static import static
schema_view = get_schema_view(
    openapi.Info(
        title="Sua API",
        default_version='v1',
        description="API utilizada para servir como backend do app de entregas App Map.",
        contact=openapi.Contact(email="danieldantefm@gmail.com"), 
    ),
    public=True,
    permission_classes=(permissions.AllowAny,permissions.BasePermission),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('',include('core.urls')),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
