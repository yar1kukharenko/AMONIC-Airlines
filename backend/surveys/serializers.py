# surveys/serializers.py

from rest_framework import serializers
from .models import SurveyQuestion, SurveyResponse

class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = ['question_code', 'question_text']


class SurveyResponseSerializer(serializers.ModelSerializer):
    question = SurveyQuestionSerializer()  # Вложенный сериализатор для вопроса
    
    class Meta:
        model = SurveyResponse
        fields = ['id', 'schedule', 'user', 'question', 'response', 'gender', 'age', 'ticket_type']
#суммарный отчет
class SummaryReportSerializer(serializers.Serializer):
    gender_data = serializers.DictField()
    age_data = serializers.DictField()
    cabin_type_data = serializers.DictField()
    destination_data = serializers.DictField()
    sample_size = serializers.IntegerField()
#детальный отчет
class DetailedReportSerializer(serializers.Serializer):
    question = serializers.CharField()
    response_totals = serializers.DictField()