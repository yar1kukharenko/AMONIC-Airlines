from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, OfficeNameListView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserActivityLogListView
from .views import LogoutView
from .views import AddUserView, EditUserRoleView
from .views import UserDashboardView
from .views import UserListView, EditUserRoleView, EnableDisableLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Логин
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('logout/', LogoutView.as_view(), name='logout'), #выход
    path('activity/', UserActivityLogListView.as_view(), name='user_activity_log_list'), #активность
    #добавление и редактирование роли пользователя
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('edit-role/<int:pk>/', EditUserRoleView.as_view(), name='edit_user_role'),
    #дашбор при входе пользователя
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    #панель администратора
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit-role/', EditUserRoleView.as_view(), name='edit_user_role'),
    path('users/<int:user_id>/toggle-login/', EnableDisableLoginView.as_view(), name='toggle_login'),

    path('offices/', OfficeNameListView.as_view(), name='office_name_list'),

    
]
