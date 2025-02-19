# surveys/urls.py

from django.urls import path
from .views import DetailedReportView, SummaryReportView, SurveyQuestionList, SurveyResponseList, SurveyResponseDetail

urlpatterns = [
    # Список вопросов опроса
    path('questions/', SurveyQuestionList.as_view(), name='survey-questions'),

    # Список всех ответов или создание нового
    path('responses/', SurveyResponseList.as_view(), name='survey-responses'),

    # Получить, обновить или удалить ответ
    path('responses/<int:pk>/', SurveyResponseDetail.as_view(), name='survey-response-detail'),

    path('summary-report/', SummaryReportView.as_view(), name='summary-report'),

    path('detailed-report/', DetailedReportView.as_view(), name='detailed-report'),
]
