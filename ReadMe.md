﻿# Резюме работы по замечаниям


## 1. Интегрировать в проект фреймворк Celery

Что сделано:

* Установлен модуль celery и коннектор для подключения к redis
* Приложение добавлено в init.py модуля orders
* Настройки приложения добавлены в settings
* В папке приложения orders/orders/ добавлен файл celery.py c настройками
* Установлен redis
* Осуществлен перенос приложения для тестирования на линукс-платформу, адрес сервера - 95.163.230.254:8000, сервер запущен. Все запросы с новым адресом и токенами в файле test\_requests\_3.http. Дальнейшее тестирование in progress..


## 2. Сделать кейс с VeiwSet и роутером.

Что сделано:

* Добавлен ProductViewSet для вывода списка продуктов (каталога) и карточки отдельного продукта.
* В urls.py зарегистрирован роутер и подключен маршрут: path('product/', include(router.urls)). Данный маршрут отрабатывает запросы раздела 4.ПРОСМОТР КАТАЛОГА ПРОДУКТОВ


## 3. Покрыть хотя бы 30% модуля views.py тестами

Что сделано:

* В папку orders/backend_app/ добавлен файл tests.py с тестами
* Для запуcка теста из командной строки терминала находясь в директории python-final-project\orders  набрать команду: python manage.py test backend_app.tests



## 4. Опробовать автогенерацию документации Open API в рамках пакета DRF-Spectacular.

Что сделано:

* Установлен пакет drf-yasg - Yet another Swagger generator, приложение подключено в settings.py
* В папку orders/orders/ добавлен файл yasg.py со схемой
* В orders/orders/urls.py добавлены маршуты для swagger и redoc, определенные в yasg.py
* Добавлены недостающие докстринги для классов и методов

В результате по ссылке http://127.0.0.1:8000/swagger/ запускается интерфейс тестирования/документирования.


## 5. Попробовать простой DRF троттлинг.

Что сделано:

В settings.py в раздел REST_FRAMEWORK добавлены настройки троттлинга:

* 'DEFAULT_THROTTLE_CLASSES'
* 'DEFAULT_THROTTLE_RATES':  
    'anon': '30/minute',
  
    'user': '60/minute'

В результате при превышении кол-ва запросов системой выводится ответ:  HTTP/1.1 429 Too Many Requests.


## 6. Добавить возможность авторизации с 1-2 социальных сетей

Что сделано:

* Установлено social-auth-app-django
* 'social_django' зарегистрировано в settings и в urls
* Там же в settings добавлен раздел AUTHENTICATION_BACKENDS и в него сервер аутентификаии ВК
* Приложение зарегистрировано в ВК
* Application Id and Application Secret прописаны в settings
Дальнейшее тестирование in progress..


## 7. Оптимизация запросов через django-silk

Не реализовано



# Комментарии к базовой поставке приложения

Приложение предоставляется в двумя базами: diploma и diploma_2.

В поставке приложения в настройках прописана база diploma_2.

diploma - пустая базой, с которой выполнены слещующие предварительные действия:


1. Установлены зависимости

2. Проведены миграции

3. Создан супер пользователь: admin 1qaz2wsx

4. Создано по одной компании:
    * "Mobilka", тип "Магазин"
    * "reStore", тип "Поставщик".

4. Зарегистрировано по одному пользователю от каждой компании

5. Проведена авторизация пользователей (см. запросы 2.1 и 2.2), полученые токены прописаны в тестовых запросах в файле test_requests.http


Если вас устраивает предварительная подготовка базы, можно перейти к шагу 10 списка тестирования ниже, в противно случае - начать с шага 1 выше.

diploma_2 - заполненная база, компании, пользователи, токены для них сформирвоаны, загружен прайс, сформирован заказ. Файл запросов для данной базы с прописанными в запросах токенами - test_requests_2.http

Для самостоятельного выполнения указанных выше шагов необходимо выполнить:

1. Установить зависимости - pip install -m requirements.txt - и запустить виртуальное окружение

2. В файле /orders/orders/settings.py в разделе DATABASES указать имя новой БД

3. Очистить папку миграций orders/backend_app/migrations

4. Из корневой папки проекта /python-final-project/orders в терминале провести миграции:

    * python manage.py makemigrations
    * python manage.py migrate

5. В терминале создать суперпользователя: python manage.py createsuperuser

6. Запустить приложение: manage.py runserver

7. Ввести адрес в браузере http://127.0.0.1:8000/admin/

8. Залогиниться под учетной записью суперюзера, созданного на шаге 5 выше.

9. Слева в меню найти BACKEND\\_APP, пункт Список команий

10. Рекомендуется добавить две компании:

    * первая:  Название - "Mobilka", тип -  "Магазин"
    * вторая: Название - "reStore", тип - "Поставщик"

    Рекомендуется создавать комании в таком же порядке и с такими же реквизитами, т.к. в дальнейшем они используются в тестовых запросах, поставляемых вместе с приложением, в противном случае запросы потребуется корректировать.

11. Открыть Visual Studio Code, а в нем файл /orders/orders/test_requests.http. В данном файле собраны запросы для тестирования функционала приложения.

12. Выполнить тестовые запросы раздела 1. РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ

13. Выполнить тестовые запросы раздела 2. АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЕЙ. При этом сохранить токены, полученные в результате выполнения запросов 2.1 и 2.2

14. Выполнить тестовые запросы раздела 3. ЗАГРУЗКА ПРАЙСА. При этом необходимо выполнить следующие условия:

    * В запросах от пользователя поставщика и покупателя необходимо подставлять соответствующие сохранненные выше токены
    * Для выполнения запроса 3.4 необходимо в файле /orders/orders/supplier1.yaml поменять id и/или name поставщика

15. Выполнить тестовые запросы раздела 4. ПРОСМОТР КАТАЛОГА ПРОДУКТОВ

16. Выполнить тестовые запросы раздела 5. ДОБАВЛЕНИЕ ПРОДУКТОВ В ЗАКАЗ

17. Выполнить тестовые запросы раздела 6. УДАЛЕНИЕ ПРОДУКТОВ ИЗ ЗАКАЗА

18. Выполнить тестовые запросы раздела 7. ПРОСМОТР ЗАКАЗОВ И ИСТОРИИ

19. Выполнить тестовые запросы раздела 8. ИЗМЕНЕНИЕ СТАТУСОВ ЗАКАЗОВ












