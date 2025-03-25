# MySQL Table Viewer

## Описание проекта
Приложение для просмотра содержимого MySQL баз данных с раздельным frontend и backend.

## Требования
- Python 3.8+
- Node.js 14+
- MySQL

## Установка Backend
1. Перейти в директорию `backend/`
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать окружение:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Настроить подключение к базе в `app.py`
6. Запустить приложение: `python app.py`

## Установка Frontend
1. Перейти в директорию `frontend/`
2. Установить зависимости: `npm install`
3. Запустить приложение: `npm start`

## Конфигурация
Обязательно замените параметры подключения к базе данных в `backend/app.py`:
- `username`: имя пользователя MySQL
- `password`: пароль
- `localhost`: хост базы данных
- `your_database`: имя базы данных

## Лицензия
MIT License