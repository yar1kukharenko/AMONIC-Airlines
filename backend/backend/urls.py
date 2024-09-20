from django.contrib import admin
from django.urls import path, include  # include для подключения внутренних приложений
from rest_framework import routers
from api.views import ItemViewSet

# Настройка маршрутов для приложения 'api'
router = routers.DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель Django
    path('api/', include(router.urls)),  # Подключаем маршруты из приложения 'api'
    path('user/', include('user.urls')),  # Подключаем маршруты из приложения 'user'
]
