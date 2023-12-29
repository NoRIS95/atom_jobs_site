# Бэкэнд-сервер для сайта по поиску вакансий компании АТОМ.

## Настройка окружения:
  1. 
  ```
  git clone https://github.com/NoRIS95/atom_jobs_site.git
  cd atom_jobs_site

  ```
  2.
  ```
  python3 -m venv env
  source ./env/bin/activate
  ```
  3. Устанавливаем Python зависимости
  ```
  pip install -r requirements.txt
  ```
  4. Создаём миграции (коммит схемы БД):
  ```
  python manage.py makemigrations
  ```
  5. Применяем миграции (накатываем коммит на БД):
  ```
  python manage.py migrate --run-syncdb 
  ```
  6. Создаем суперпользователя:
  ```
  python manage.py createsuperuser
  ```

## Сервисы

  1. Выгрузка вакансий из hh (должен периодически запускаться, например, в кроне):
  ```
  python manage.py parse_hh
  ```
  2. Индексирование вакансий (нужно для поисковика):
  Первый раз
  ```
  python manage.py rebuild_index
  ```
  Последующие
  ```
  python manage.py update_index
  ```
  3. Веб-сервер:
  ```
  python manage.py runserver
  ```

## REST API

### Список вакансий
```GET /api/jobs/```

### Поиск вакансий
```GET /api/jobs/search?q=```

### Отклик
```POST /submit/<int:job_id>```

Параметры:
* firstname
* surname
* lastname
* email
* phone
* application_text

FILES:
* cv
