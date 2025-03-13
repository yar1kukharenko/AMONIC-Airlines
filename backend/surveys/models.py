# surveys/models.py

from django.db import models
from flight.models import Schedule
from user.models import User

# Модель для вопросов опроса
class SurveyQuestion(models.Model):
    QUESTION_CHOICES = [
        ('Q1', 'Пожалуйста, оцените самолет, на котором Вы летели с AMONIC Airlines'),
        ('Q2', 'Как бы Вы оценили наших борт проводников'),
        ('Q3', 'Как бы Вы оценили развлечения во время полета'),
        ('Q4', 'Пожалуйста, оцените цену на билет Вашего маршрута'),
    ]
    question_code = models.CharField(max_length=2, choices=QUESTION_CHOICES, unique=True)
    question_text = models.TextField()

    def __str__(self):
        return self.get_question_code_display()

# Модель для ответов на опрос
class SurveyResponse(models.Model):
    RATING_CHOICES = [
        (1, 'Outstanding / Великолепно'),
        (2, 'Very Good / Очень хорошо'),
        (3, 'Good / Хорошо'),
        (4, 'Adequate / Нормально'),
        (5, 'Needs Improvement / Необходимо улучшить'),
        (6, 'Poor / Плохо'),
        (7, 'Don’t know / Не знаю'),
        (0, 'Не ответил')
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)  # Рейс
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Пользователь может быть анонимным
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)  # Вопрос опроса
    response = models.IntegerField(choices=RATING_CHOICES, default=0)  # Оценка
    gender = models.CharField(max_length=10, blank=True, null=True)  # Пол (опционально)
    age = models.IntegerField(blank=True, null=True)  # Возраст (опционально)
    ticket_type = models.CharField(max_length=50, blank=True, null=True)  # Тип билета (эконом, бизнес и т.д.)

    def __str__(self):
        return f"Response for {self.question} by {self.user if self.user else 'Anonymous'}"
