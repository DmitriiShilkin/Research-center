## Тестовое задание от Research Center (результат):
1. Спроектирован и реализован на Python сервис, предоставляющий REST API интерфейс с методами:
- `GET /rc/v1/rate_alert/` вывод списка записей о повышении цены;
- `PATCH /rc/v1/rate_alert/{rate_alert_id}/` редактирование записи о повышении цены;
- `DELETE /rc/v1/rate_alert/{rate_alert_id}/` удаления записи о повышении цены;
- `GET /rc/v1/search/rate_alert/` поиск записи о повышении цены по ее заголовку `title`;
- `POST /rc/v1/user/` регистрация пользователя;
- `POST /rc/v1/login/` аутентификация и авторизация пользователя;
- `DELETE /rc/v1/logout/` выход пользователя из системы.
2. Сервер работает через REST API, для передачи данных используется формат json. 
3. Web-сервер реализован на асинхронном web-фреймворке fastapi. 
4. В коде проставлены type hints.
5. Реализован мониторинг цен на биржах:
- https://www.binance.com/ru;
- https://coinmarketcap.com/ru/;
- https://www.bybit.com/ru-RU/;
- https://www.gate.io/ru;
- https://www.kucoin.com/ru.  
При этом отслеживаются следующие пары валют:
- BTC/USDT;
- BTC/ETH;
- BTC/XMR;
- BTC/SOL;
- BTC/RUB;
- BTC/DOGE.
6. При росте курса >= 0.03% на email `lakritsa@gmail.com` отправляется письмо, в котором указана стоимость накоплений 
в валюте, разница и название биржи. Для перехвата email используется MailCatcher.
7. Для получения данных с бирж выполняется задача по расписанию, реализованная с помощью библиотеки schedule в 
отдельном потоке.
8. Каждое повышение цены записывается в базу данных PostgreSQL.
9. Используемый формат записи:
```
key_json = {
    'title': str,
    'kash': [{
        'price': decimal, 
        'minmax': [{ 
            'min_price': decimal,
            'max_price': decimal
        }]
    ],
    'difference': decimal, 
    'total_amount': decimal,
    'coins': [{
        'BTC': 'USDT',
        'BTC': 'ETH',
        'BTC': 'XMR',
        'BTC': 'SOL',
        'BTC': 'RUB',
        'BTC': 'DOGE'
    }],
    'date': str
} 
```
10. Реализован мониторинг цен на желаемые товары:
- копье,
- дуршлаг,
- красные носки,
- леска для спиннинга.   
Поиск ведется на маркетплейсах: 
- https://www.wildberries.ru, 
- https://www.ozon.ru,
- https://market.yandex.ru.   
Из результатов поиска отбирается по 1 карточке товара с наименьшей ценой.
11. В качестве ORM используется Tortoise ORM.
12. Для создания и управления миграциями используется Aerich.
13. Запуск сервиса и требуемой им инфраструктуры производится в докер-контейнерах.


### Инструкция для запуска
1. Предварительные настройки:
- зарегистрироваться на сервисе https://pro.coinmarketcap.com/signup/?plan=0 и получить API Key, открыть файл 
переменных окружения `src/.env` и записать полученный ключ для параметра `X_CMC_PRO_API_KEY=`;
- настроить требуемую периодичность проверки задач и бирж в файле `src/constants/scheduler.py` с помощью констант  
`CHECK_INTERVAL_SECONDS`, `RUN_INTERVAL_MINUTES`.
2. Запустить сервис, выполнив в консоли linux из корневой папки команду `bash start.sh`.  
Дождаться надписи `Application startup complete`.
3. Проверить работу API, перейдя в браузере по адресу http://127.0.0.1:8000/rc/docs.
4. Перехваченную почту можно смотреть в браузере по адресу http://127.0.0.1:1080. Почта доступна пока работает сервис.
После перезапуска сервиса ранее полученные письма удаляются.
5. Завершить работу сервиса, нажав клавиши `ctrl+c`.


### Стек
- Python v3.11.8
- fastapi v0.115.0
- tortoise-orm v0.21.6
- aerich v0.7.2
- schedule v1.2.2
- MailCatcher v0.8.2
- uvicorn v0.30.6
- selenium v4.25.0
- beautifulsoup v4.12.3
