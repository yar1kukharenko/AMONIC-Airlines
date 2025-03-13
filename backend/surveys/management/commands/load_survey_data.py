# surveys/management/commands/load_survey_data.py

import csv
from django.core.management.base import BaseCommand
from surveys.models import SurveyQuestion, SurveyResponse
from flight.models import Airport, Schedule

class Command(BaseCommand):
    help = 'Create survey questions and load survey data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing survey data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # 1. Создание вопросов опроса
        self.create_survey_questions()

        # 2. Загрузка данных из CSV
        self.load_survey_data(csv_file)

    def create_survey_questions(self):
        """Создаем вопросы для опроса"""
        questions = [
            ('Q1', 'Пожалуйста, оцените самолет, на котором Вы летели с AMONIC Airlines'),
            ('Q2', 'Как бы Вы оценили наших борт проводников'),
            ('Q3', 'Как бы Вы оценили развлечения во время полета'),
            ('Q4', 'Пожалуйста, оцените цену на билет Вашего маршрута')
        ]
        
        for code, text in questions:
            SurveyQuestion.objects.get_or_create(
                question_code=code,
                defaults={'question_text': text}
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added or verified question {code}'))

    def load_survey_data(self, csv_file):
        """Загружаем данные из CSV файла"""
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок

            for row in reader:
                departure_code = row[0]  # Город отправления
                arrival_code = row[1]    # Город прибытия
                age = int(row[2])        # Возраст
                gender = row[3]          # Пол
                travel_class = row[4]    # Класс обслуживания
                q1_response = int(row[5])  # Ответ на Q1
                q2_response = int(row[6])  # Ответ на Q2
                q3_response = int(row[7])  # Ответ на Q3
                q4_response = int(row[8])  # Ответ на Q4

                # Получаем аэропорты
                departure_airport = Airport.objects.get(IATA_code=departure_code)
                arrival_airport = Airport.objects.get(IATA_code=arrival_code)

                # Получаем расписание на основе маршрута
                schedule = Schedule.objects.filter(
                    route__departure_airport=departure_airport,
                    route__arrival_airport=arrival_airport
                ).first()

                # Проверяем, найдено ли расписание
                if not schedule:
                    self.stdout.write(self.style.WARNING(f'Schedule not found for route from {departure_code} to {arrival_code}. Skipping this entry.'))
                    continue

                # Создаем записи ответов для вопросов Q1-Q4
                for question_code, response in zip(['Q1', 'Q2', 'Q3', 'Q4'], [q1_response, q2_response, q3_response, q4_response]):
                    question = SurveyQuestion.objects.get(question_code=question_code)
                    SurveyResponse.objects.create(
                        schedule=schedule,
                        user=None,  # анонимный пользователь
                        question=question,
                        response=response,
                        gender=gender,
                        age=age,
                        ticket_type=travel_class
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully imported response for {question_code}.'))
