# Сервис для аренды боксов на складе
Код для сервиса по аренде боксов и сезонного хранения вещей.

Пример сайта можно глянуть [тут](https://selfstorageservice.pythonanywhere.com/)

## Технологии
1. Django
2. HTML/CSS/JS

## Как запустить локально
1. Сделать `git clone`
2. Создать виртуальное окружение `python -m venv venv`
3. Активировать виртуальное окружение 
4. Установить библиотеки через `pip install -r requirements.txt`
5. Создать файл `.env` (пример заполнения в `.env.sample`)
6. Запустить миграции `python manage.py migrate`
7. Запустить приложение `python manage.py runserver`

## Цель проекта
Проект выполнен в обучающих целях для сайта [dvmn](https://dvmn.org/)
