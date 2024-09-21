import pandas as pd
import os
from django.core.management.base import BaseCommand
from user.models import User, Role, Office, Country
from django.utils.dateparse import parse_date
from django.conf import settings

class Command(BaseCommand):
    help = 'Load users from a CSV file'

    def handle(self, *args, **kwargs):
        # Определение пути к CSV файлу в папке data
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'UserData.csv')

        # Указываем заголовки вручную, так как они отсутствуют в файле CSV
        column_names = ['Role', 'Email', 'Password', 'Firstname', 'Lastname', 'City', 'Birthdate', 'Active']

        # Загружаем данные из CSV с указанием заголовков
        data = pd.read_csv(csv_file_path, names=column_names)

        for _, row in data.iterrows():
            # Определение роли пользователя
            role_title = row['Role']
            role, created = Role.objects.get_or_create(title=role_title)

            # Определение офиса пользователя
            country_name = row['City']  # Название города в CSV связано с Country
            country, created = Country.objects.get_or_create(name=country_name)

            office, created = Office.objects.get_or_create(country=country, title=row['City'])

            # Создаем пользователя
            user = User.objects.create(
                email=row['Email'],
                firstname=row['Firstname'],
                lastname=row['Lastname'],
                birthdate=parse_date(row['Birthdate']),
                active=row['Active'] == 1,
                role=role,
                office=office,
            )

            # Преобразуем пароль в строку, чтобы избежать ошибок
            user.set_password(str(row['Password']))
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded users from CSV'))
