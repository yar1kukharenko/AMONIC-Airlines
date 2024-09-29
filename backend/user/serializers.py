from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserActivityLog

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
# Сериализатор для создания пользователей
class AddUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'office', 'birthdate', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            office=validated_data['office'],
            birthdate=validated_data['birthdate'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Сериализатор для редактирования роли пользователя
class EditRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('role',)

    def validate_role(self, value):
        # Администратор не может изменить роль другого пользователя на администратора
        request_user = self.context['request'].user
        if value.title == 'Administrator' and not request_user.is_superuser:
            raise serializers.ValidationError("Администратор не может назначать других администраторов.")
        return value

#отображения активности
class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = [ 'login_time', 'logout_time', 'duration', 'logout_reason']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'role', 'email', 'office']

class EditRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']