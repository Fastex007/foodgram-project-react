# FOODGRAM

![Foodgram Workflow](https://github.com/Fastex007/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### http://62.84.116.251

Сервис обмена рецептами.
После регистрации пользователям будут доступны возможности публиковать свои 
рецепты, подписываться на других авторов, сохранять рецепты в избранное,
скачивать список покупок для повторения рецептов.

## Подготовка проекта
Получить проект
```
git@github.com:Fastex007/foodgram-project-react.git
```

### Настройки проекта
- Создать миграции
```
python manage.py makemigrations
```
- Применить миграции
```
python manage.py migrate
```
- Создать суперпользователя
```
python manage.py createsuperuser
```
- Импортировать ингредиенты
```
python manage.py import_data
```
- Собрать статические данные
```
python manage.py collectstatic
```

### Переменные окружения
```
DEBUG=False
SECRET_KEY=<secret key>
ALLOWED_HOSTS=[*]
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<db name>
POSTGRES_USER=<db user>
POSTGRES_PASSWORD=<db password>
DB_HOST=<db host>
DB_PORT=<db port>
```

## Технологии
- [![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
- [![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
- [![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
- [![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
- [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
- [![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
- [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
- [![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

### Автор
https://github.com/Fastex007/

### Ревьюэру
- логин: admin
- пароль: admin