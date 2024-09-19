1. Установить Python (если не установлен).
2. Создать и активировать виртуальное окружение.
3. Установить зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```
4. Установить PostgreSQL соответствующей версии.

5. Создать базу данных и пользователя в PostgreSQL:  
Запустить консоль psql и выполнить команды для создания базы данных и пользователя:

```sql
CREATE DATABASE amonic;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myuser;
```

6. Создать в корневой директории проекта файл .env с необходимыми переменными окружения. Пример файла .env:
```
DB_NAME=myproject
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
```

7. Запустить миграции для настройки базы данных:
```bash
python manage.py migrate
```
8. Запустить сервер и проверить работу приложения:
```bash
python manage.py runserver
```
