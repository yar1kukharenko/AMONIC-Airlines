# surveys/admin.py

from django.contrib import admin
from .models import SurveyQuestion, SurveyResponse

# Регистрация модели вопросов
@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_code', 'question_text')
    search_fields = ('question_code', 'question_text')

# Регистрация модели ответов
@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'user', 'question', 'response', 'gender', 'age', 'ticket_type')
    list_filter = ('response', 'gender', 'age', 'ticket_type')
    search_fields = ('user__email', 'schedule__flight_number')
