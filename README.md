# Веб-сервис, принимающий заказы на бронирование столиков в ресторане.

### Функционал публичный:

1. Подбор столика на основе типа столика (маленький, средний и большой), количеству мест и диапазону цены.
2. Заявка на бронирование столика.
3. Отмена бронирования.

### Функционал администратора:

1. Регистрация работника.
2. Авторизация (предоставляется JWT токен).
3. Просмотр всех столиков в ресторане.
4. Добавление столов.
5. Закрыть столик.
6. Забронировать столик (подтвердить бронь).
7. Изменить стоимость столика.

##### **Предполагается, что при получении заявки на бронирование, она перенаправляется на подтверждение рабонику. После его подтверждения отсылается письмо на почту из заявки с кнопкой на отмену брони.**

### Описание работы веб-сервиса:

* /show/

Принимает POST запросы в виде:

```
{
 types: str
 seats: int
 cost1: float
 cost2: float
}
```

В ответ отдает список, состоящий из словарей, каждый словарь характеризует отдельный стол (id, seats, cost).

* /order/

Принимает POST запросы в виде:

```
{
 id: int
 types: str
 mail: str
}
```

В ответ сервер отправляет письмо на почту с информацией, где есть кнопка отмены, которая отменяет заказ.

Пример сообщения:

![image.png](./assets/image.png)

* /cancel/

Принимает GET запрос c параметрами `id`, `types` и `mail`.

```
{
 id: int
 types: str
 mail: str
}
```

В ответ сервер отправляет письмо на почту с информацией, что заказ отменен и детали заказа.

Пример сообщения:

![image.png](./assets/1658441768582-image.png)


* /registr/

Принимает POST запросы в виде:

```
{
 username: str
 password1: str
 password2: str
}
```

В случае успешного запроса отвечает в виде:

```
{
'username': username, 
'password': password1
}
```

* /login/

Принимает POST запросы в виде:

```
{
 username: str
 password: str
}
```

В случае успешного запроса отвечает токенами:

```
{
'access_token': access_token,
'refresh_token': refresh_token
}
```

* /refresh_token/

Принимает GET запрос с параметром `refresh_token` требуется `access_token`.

* /show_all/

Принимает GET запрос требуется `access_token`.

* /close/

Принимает POST запросы в виде:

```
{
 types: str
 id: int
}

```

* /change_price/

Принимает POST запросы в виде:

```
{
 types: str
 id: int
 cost: float
}
```

* /add_tables/

Принимает POST запросы в виде:

```
{
 types: str
 count: int
 seats: int
 cost: float
}
```

* /change_table/

Принимает POST запросы в виде:

```
{
 types: str
 id: int
 seats: int
 cost: float
}
```

* /booking/

Принимает POST запросы в виде:

```
{
 types: str
 id: int
 booking: bool
}
```

В случае ошибок на любом endpoint сервер отвечает сообщением вида:

```
{
 'Event': 'Error',
 'Detail': error,
 'Arguments': args
}
```

### Параметры БД и секрет для токена, а также данные для почты берутся из файла .env

### Запуск на локальной машине можно запустить с помощью команды `python main.py` или `python3 main.py`, требуется находиться в папке с проектом.
