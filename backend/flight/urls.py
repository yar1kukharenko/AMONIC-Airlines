from django.urls import path
from .views import ScheduleListView, ScheduleDetailView, UpdateScheduleStatusView, ImportScheduleChangesView

urlpatterns = [
    path('schedules/', ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('schedules/<int:pk>/status/', UpdateScheduleStatusView.as_view(), name='schedule-status'),
    path('schedules/import/', ImportScheduleChangesView.as_view(), name='schedule-import'),
]
