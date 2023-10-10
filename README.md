#  Yaposts
Социальная сеть для блогеров. Сайт, на котором можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора. Пользователи смогут заходить на чужие страницы, подписываться на авторов и комментировать их записи. Автор может выбрать имя и уникальный адрес для своей страницы. Есть возможность модерировать записи и снимать с публикации. 

## Технологии

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-464646?style=flat-square&logo=django)](https://www.django-rest-framework.org/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/)
[![Aiogram](https://img.shields.io/badge/-Aiogram-464646?style=flat-square&logo=Aiogram)](https://aiogram.dev/)
[![ckeditor4](https://img.shields.io/badge/-Ckeditor4-464646?style=flat-square&logo=ckeditor4)](https://ckeditor.com/)
[![Pillow](https://img.shields.io/badge/-Pillow-464646?style=flat-square&logo=Pillow)](https://pypi.org/project/Pillow/)
[![Flake8](https://img.shields.io/badge/-Flake8-464646?style=flat-square&logo=Flake8)](https://flake8.pycqa.org/en/latest/)
[![Recaptcha](https://img.shields.io/badge/-Recaptcha-464646?style=flat-square&logo=Recaptcha)](https://pypi.org/project/django-recaptcha/)
[![bootstrap](https://img.shields.io/badge/-Bootstrap-464646?style=flat-square&logo=bootstrap)](https://getbootstrap.com/)

## Описание
- Можно создать свою страницу.
- После регистрации пользователь получает свой профайл, то есть получает свою страницу.
- Если на нее зайти, то можно посмотреть все записи автора.
- Пользователи могут заходить на чужие страницы, подписываться на авторов и комментировать их записи.
- Автор может выбрать для своей страницы имя и уникальный адрес.
- Есть возможность модерировать записи и блокировать пользователей, если начнут присылать спам.(реализовано через админ-панель)
- Записи можно отправить в сообщество и посмотреть там записи разных авторов.
- API дает возможность просмотра постов, авторов, групп, регистрацию пользователей, добавление постов.
- Телеграм бот выводит информацию о постах, автогах и группах.

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команды:
```
python manage.py runserver
python manage.py run_bot
```
Документация по API:
```
http://127.0.0.1:8000/redoc/
```

### Автор
Евгений Березовский
