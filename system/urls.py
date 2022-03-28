# from django.contrib import admin as ad
from baton.autodiscover import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from eld.view import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="FastLogz API",
      default_version='v1',
      description="Fastlogz's endpoints",
      terms_of_service="https://trello.com/b/oUMXY4je/fastlogz",
      contact=openapi.Contact(email="tanlanganasarlar@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

api = [
    path('', include('eld.urls')),
    path('event/', include('event.urls')),
    path('log/', include('log.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]

urlpatterns = [
    path('swagger<format>\.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('api/', include(api)),
    path('search/', include('search.urls')),
    path('', views.hello),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

admin.site.site_url = 'https://fastslogz.napaautomotive.uz/'
