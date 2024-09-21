from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role, Office, Country
from .models import UserActivityLog

# Кастомный админ для модели User
class UserAdmin(BaseUserAdmin):
    # Какие поля отображать в списке пользователей в админке
    list_display = ('email', 'firstname', 'lastname', 'is_staff', 'active', 'role', 'office')

    # Поля для фильтрации
    list_filter = ('is_staff', 'active', 'role', 'office')

    # Поля для поиска
    search_fields = ('email', 'firstname', 'lastname')

    # Порядок полей на странице редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('firstname', 'lastname', 'birthdate')}),
        (_('Office and Role'), {'fields': ('office', 'role')}),
        (_('Permissions'), {'fields': ('active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля, которые требуются при создании нового пользователя через админку
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstname', 'lastname', 'is_staff', 'active', 'role', 'office'),
        }),
    )

    # Порядок сортировки записей
    ordering = ('email',)


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'duration', 'logout_reason')
    search_fields = ('user__email',)
    list_filter = ('login_time', 'logout_time')

# Регистрируем модели в админке
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Office)
admin.site.register(Country)
