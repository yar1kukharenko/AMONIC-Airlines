from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import timedelta
from .models import UserActivityLog, User, Role
from .serializers import (
    RegisterSerializer, 
    UserActivityLogSerializer, 
    AddUserSerializer, 
    EditRoleSerializer
)
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

# Представление для регистрации пользователей
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Кастомизация JWT токенов (если необходимо)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # Добавить email в токен
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.get_user(request.data['email'])  # Находим пользователя по email
        if user:
            UserActivityLog.objects.create(user=user, login_time=timezone.now())
        return response

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

# Представление для добавления пользователей
class AddUserView(generics.CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [IsAdminUser]  # Только администраторы могут добавлять пользователей

    def perform_create(self, serializer):
        role = Role.objects.get(title='User')  # Назначаем роль "User" по умолчанию
        serializer.save(role=role)

# Представление для изменения роли пользователя
class EditUserRoleView(generics.UpdateAPIView):
    serializer_class = EditRoleSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

# Представление для списка активности пользователей
class UserActivityLogListView(generics.ListAPIView):
    """
    Эндпоинт для просмотра списка активности пользователей.
    
    Доступен только администраторам. Позволяет получить список всех сессий активности пользователей.
    """
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Получить список всех активностей пользователей (доступно только администраторам).",
        responses={200: UserActivityLogSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Представление для выхода пользователя
class LogoutView(APIView):
    """
    Эндпоинт для выхода пользователя из системы.
    
    После вызова этого метода пользователь будет разлогинен, и его сессия будет завершена.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Завершить активную сессию пользователя.",
        responses={
            200: "Пользователь успешно вышел из системы.",
            400: "Активной сессии не найдено."
        }
    )
    def post(self, request):
        activity_log = UserActivityLog.objects.filter(user=request.user, logout_time__isnull=True).first()
        if not activity_log:
            return Response({"error": "No active session found for this user."}, status=400)
        
        activity_log.logout_time = timezone.now()
        activity_log.logout_reason = "User logged out successfully"
        activity_log.save()
        return Response({"message": "User logged out successfully."}, status=200)

# Представление для дашборда пользователя
class UserDashboardView(APIView):
    """
    Эндпоинт для просмотра дашборда пользователя.
    
    Возвращает информацию о времени, проведенном в системе, и количестве сбоев (некорректных выходов) за последние 30 дней.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить информацию о дашборде пользователя: полное имя, общее время в системе, количество сбоев и логи активности за последние 30 дней.",
        responses={
            200: "Информация успешно получена.",
            401: "Необходима авторизация."
        }
    )
    def get(self, request):
        user = request.user
        today = timezone.now()
        thirty_days_ago = today - timedelta(days=30)
        activity_logs = UserActivityLog.objects.filter(user=user, login_time__gte=thirty_days_ago)

        total_time_in_system = sum([log.duration for log in activity_logs if log.duration], timedelta())
        crash_count = activity_logs.filter(logout_reason__isnull=False).count()

        data = {
            "full_name": f"{user.firstname} {user.lastname}",
            "time_spent_on_system": str(total_time_in_system),
            "number_of_crashes": crash_count,
            "activity_logs": UserActivityLogSerializer(activity_logs, many=True).data
        }

        return Response(data)

#для админ панели
class UserListView(generics.ListAPIView):
    """
    Эндпоинт для просмотра списка пользователей.

    Этот эндпоинт позволяет администраторам просматривать список всех пользователей с возможностью фильтрации по офисам.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['office']  # Фильтрация по офисам

    @swagger_auto_schema(
        operation_description="Получить список пользователей с возможностью фильтрации по офису.",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class EditUserRoleView(generics.UpdateAPIView):
    """
    Эндпоинт для изменения роли пользователя.

    Этот эндпоинт позволяет администраторам изменять роль существующих пользователей.
    """
    queryset = User.objects.all()
    serializer_class = EditRoleSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Изменить роль пользователя. Администраторы могут обновлять роль для существующих пользователей.",
        request_body=EditRoleSerializer,
        responses={200: "Роль пользователя успешно изменена", 400: "Ошибки валидации"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class EnableDisableLoginView(APIView):
    permission_classes = [permissions.IsAdminUser]
    """
    Эндпоинт для отключения авторизации пользователя.

    """
    @swagger_auto_schema(
        operation_description="Отключение авторизации пользователя.(кнопка Enable/Disable login) ",
        request_body=RegisterSerializer,
    )

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.active = not user.active  # Переключаем статус активности
            user.save()
            status_msg = "enabled" if user.active else "disabled"
            return Response({"message": f"User login {status_msg}."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)