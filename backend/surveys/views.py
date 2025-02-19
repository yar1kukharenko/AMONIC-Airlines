# surveys/views.py

from rest_framework import generics
from .models import SurveyResponse, SurveyQuestion
from .serializers import SurveyResponseSerializer, SurveyQuestionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import SurveyResponse
from .serializers import SummaryReportSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from .models import SurveyResponse, SurveyQuestion
from .serializers import DetailedReportSerializer

# Получить список всех вопросов
class SurveyQuestionList(generics.ListAPIView):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer

# Получить все ответы на опросы
class SurveyResponseList(generics.ListCreateAPIView):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer

# Получить, обновить или удалить конкретный ответ
class SurveyResponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer


class SummaryReportView(APIView):

    def get(self, request, *args, **kwargs):
        # Подсчет количества по полу
        gender_data = SurveyResponse.objects.values('gender').annotate(total=Count('id'))

        # Классификация по возрастным группам
        age_data = {
            '18-24': SurveyResponse.objects.filter(age__gte=18, age__lt=25).count(),
            '25-39': SurveyResponse.objects.filter(age__gte=25, age__lt=40).count(),
            '40-59': SurveyResponse.objects.filter(age__gte=40, age__lt=60).count(),
            '60+': SurveyResponse.objects.filter(age__gte=60).count(),
        }

        # Классификация по типам кабин
        cabin_type_data = SurveyResponse.objects.values('ticket_type').annotate(total=Count('id'))

        # Классификация по пунктам назначения
        destination_data = SurveyResponse.objects.values('schedule__route__arrival_airport__IATA_code').annotate(total=Count('id'))

        # Общее количество записей
        sample_size = SurveyResponse.objects.count()

        # Формирование ответа
        data = {
            'gender_data': {item['gender']: item['total'] for item in gender_data},
            'age_data': age_data,
            'cabin_type_data': {item['ticket_type']: item['total'] for item in cabin_type_data},
            'destination_data': {item['schedule__route__arrival_airport__IATA_code']: item['total'] for item in destination_data},
            'sample_size': sample_size
        }

        serializer = SummaryReportSerializer(data)
        return Response(serializer.data)

class DetailedReportView(APIView):

    def get(self, request, *args, **kwargs):
        # Получение фильтров из запроса
        gender = request.query_params.get('gender', None)  # Пол
        age_group = request.query_params.get('age_group', None)  # Возрастная группа
        cabin_type = request.query_params.get('cabin_type', None)  # Тип кабины
        destination = request.query_params.get('destination', None)  # Пункт назначения
        time_period = request.query_params.get('time_period', None)  # Период времени

        # Построение фильтрации
        filters = Q()
        if gender:
            filters &= Q(gender=gender)
        if age_group:
            if age_group == '18-24':
                filters &= Q(age__gte=18, age__lt=25)
            elif age_group == '25-39':
                filters &= Q(age__gte=25, age__lt=40)
            elif age_group == '40-59':
                filters &= Q(age__gte=40, age__lt=60)
            elif age_group == '60+':
                filters &= Q(age__gte=60)
        if cabin_type:
            filters &= Q(ticket_type=cabin_type)
        if destination:
            filters &= Q(schedule__route__arrival_airport__IATA_code=destination)
        if time_period:
            # Допустим, time_period передается в формате YYYY-MM, фильтруем по дате рейса
            year, month = time_period.split('-')
            filters &= Q(schedule__date__year=year, schedule__date__month=month)

        # Вопросы опроса
        questions = SurveyQuestion.objects.all()
        report_data = []

        # Группировка данных по каждому вопросу
        for question in questions:
            response_totals = SurveyResponse.objects.filter(filters, question=question).values('response').annotate(total=Count('id'))

            # Формируем структуру ответа
            report_data.append({
                'question': question.question_text,
                'response_totals': {item['response']: item['total'] for item in response_totals}
            })

        serializer = DetailedReportSerializer(report_data, many=True)
        return Response(serializer.data)