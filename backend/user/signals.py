from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivityLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print(f"User {user.email} logged in at {timezone.now()}")  # Для отладки
    UserActivityLog.objects.create(user=user)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    print(f"User {user.email} logged out at {timezone.now()}")  # Для отладки
    activity_log = UserActivityLog.objects.filter(user=user, logout_time__isnull=True).first()
    if activity_log:
        activity_log.logout_time = timezone.now()
        activity_log.logout_reason = "User logged out successfully"
        activity_log.save()
