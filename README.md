# praktikum_new_diplom
# Сайт Foodgram, «Продуктовый помощник»
### Описание
Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
### Сайт Foodgram
http://myfoodgramnetwork.ddns.net
### Документация
http://myfoodgramnetwork.ddns.net/api/docs/
### Администрирование
http://myfoodgramnetwork.ddns.net/admin/
Логин:  admin
Пароль: admin
### Технологии
Python 3.7
Django 2.2.19
### Запуск проекта в dev-режиме
- Клонировать репозиторий GitHub: 
```
git clone git@github.com:EleonoraVal/foodgram-project-react.git
``` 
- Создать файл .env в папке infra:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
``` 
- В папке infra собрать контейнеры:
```
docker-compose up -d
```
- Выполнить минрации, создать суперпользователя, собрать статику и загрузить ингредиенты:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py load_data
```
### Авторы
Элеонора Дырда 
