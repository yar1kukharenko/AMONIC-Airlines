from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Логин
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
