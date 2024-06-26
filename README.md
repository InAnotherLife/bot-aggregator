# Телеграм бот для агрегации статистических данных о зарплатах сотрудников

https://github.com/InAnotherLife/bot-aggregator

https://t.me/JohnWooooo

[![Bot aggregator workflow](https://github.com/InAnotherLife/bot-aggregator/actions/workflows/main.yml/badge.svg)](https://github.com/InAnotherLife/bot-aggregator/actions/workflows/main.yml)

## О проекте
Приложение представляет собой телеграм бот для агрегации статистических данных о зарплатах сотрудников по временным промежуткам (месяцам, дням, часам).\
Приложение разработано на языке Python версии 3.9. Код программы находится в папке src.\
Код покрыт тестами. Для написания тестов использовался фреймворк Pytest.

## Стек
* Python 3.9
* MongoDB
* Asyncio
* Aiogram

## Запуск приложения
В корне проекта создать файл .env. Пример заполнения файла:
```
URI='mongodb://localhost:27017/'
TOKEN='6228509215:AAEzMiu5PePr3PXs9LNHH6XTenG4KTcRKLM'
```

Необходимо создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Перейти в папку src и запустить телеграм бот:
```
cd src
python bot.py
```

## Работа с приложением
Бот принимает на вход следующие данные в формате json:

- Дату и время старта агрегации в ISO формате (dt_from)
- Дату и время окончания агрегации в ISO формате (dt_upto)
- Тип агрегации (group_type), возможные варианты: month, day, hour

Пример входных данных:

```
{
    "dt_from":"2022-09-01T00:00:00",
    "dt_upto":"2022-12-31T23:59:00",
    "group_type":"month"
}
```

Пример ответа бота:
```
{
    "dataset": [5906586, 5515874, 5889803, 6092634],
    "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]
}
```

## Запуск тестов
Для запуска тестов необходимо перейти в папку src и выполнить команду:
```
pytest -v tests.py
```