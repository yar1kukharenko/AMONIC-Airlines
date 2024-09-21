from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import ItemViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()

# Настройка Swagger документации
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API documentation with JWT",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель Django
    path('api/', include('api.urls')),  # Подключаем маршруты из приложения 'api'
    #path('user/', include('user.urls')),  # Подключаем маршруты из приложения 'user'
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
]

