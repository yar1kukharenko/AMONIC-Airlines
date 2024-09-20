from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Менеджер для работы с кастомной моделью пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError(_('У пользователя должен быть email адрес'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Модель для ролей пользователей
class Role(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Модель для стран
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Модель для офисов
class Office(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

# Модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    office = models.ForeignKey('Office', on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Административный флаг
    is_superuser = models.BooleanField(default=False)  # Флаг суперпользователя
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Указываем уникальное имя для обратной связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Указываем уникальное имя для обратной связи
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Для авторизации будет использоваться email
    REQUIRED_FIELDS = ['firstname', 'lastname']  # Эти поля обязательны при создании суперпользователя

    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на пользователя
    login_time = models.DateTimeField(default=timezone.now)  # Время входа
    logout_time = models.DateTimeField(null=True, blank=True)  # Время выхода
    duration = models.DurationField(null=True, blank=True)  # Длительность сессии
    logout_reason = models.CharField(max_length=255, blank=True, null=True)  # Причина некорректного выхода

    def save(self, *args, **kwargs):
        # При сохранении, если есть время выхода, рассчитываем длительность сессии
        if self.logout_time:
            self.duration = self.logout_time - self.login_time
        super(UserActivityLog, self).save(*args, **kwargs)

    def __str__(self):
        return f'Activity for {self.user.email} from {self.login_time} to {self.logout_time}'