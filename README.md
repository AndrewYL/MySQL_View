﻿# MySQL Table Viewer

## Описание проекта
MySQL Table Viewer — это интерактивное веб-приложение для просмотра и редактирования данных в MySQL базах данных. Приложение разработано с использованием современных технологий и имеет удобный пользовательский интерфейс для работы с таблицами MySQL.

## Возможности
- 📊 Подключение к разным базам данных
- 📋 Отображение списка всех таблиц в выбранной базе данных
- 📑 Просмотр данных таблиц в удобном табличном виде
- 🔍 Поиск по всем данным таблицы
- 🔄 Сортировка данных по любому столбцу
- ➕ Добавление новых записей через интуитивно понятную форму
- ✏️ Редактирование существующих записей
- 🗑️ Удаление записей
- 📱 Адаптивный дизайн для работы на различных устройствах

## Технологии

### Backend
- Python 3.8+
- Flask (веб-фреймворк)
- MySQL Connector (для работы с базами данных)
- dotenv (для управления конфигурацией)

### Frontend
- React.js
- Axios (для HTTP-запросов)
- React Icons (для визуальных элементов)
- CSS3 (для стилизации интерфейса)

## Требования
- Python 3.8+
- Node.js 14+
- MySQL сервер
- Современный веб-браузер

## Установка и запуск

### Backend
1. Перейдите в директорию `backend`:
   ```sh
   cd backend
   ```
2. Создайте виртуальное окружение Python:
   ```sh
   python -m venv .venv
   ```
3. Активируйте виртуальное окружение:
   - **Windows**:
     ```sh
     .venv\Scripts\activate
     ```
   - **Linux/MacOS**:
     ```sh
     source .venv/bin/activate
     ```
4. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
5. Создайте файл `.env` в директории `backend` со следующим содержимым:
   ```ini
   MYSQL_HOST=localhost
   MYSQL_USER=ваше_имя_пользователя
   MYSQL_PASSWORD=ваш_пароль
   MYSQL_DB=имя_базы_данных
   MYSQL_PORT=3306
   ```
6. Запустите сервер:
   ```sh
   python app.py
   ```
7. Сервер будет доступен по адресу: [http://localhost:5000](http://localhost:5000)

### Frontend
1. Перейдите в директорию `frontend`:
   ```sh
   cd frontend
   ```
2. Установите зависимости:
   ```sh
   npm install
   ```
3. Запустите приложение:
   ```sh
   npm start
   ```
4. Приложение откроется в браузере по адресу: [http://localhost:3000](http://localhost:3000)

## Использование

### Выбор базы данных
- При запуске приложения выберите базу данных из выпадающего списка

### Выбор таблицы
- После выбора базы данных, выберите таблицу для просмотра

### Просмотр и поиск данных
- Данные отображаются в виде таблицы
- Используйте поле поиска для фильтрации данных по любому значению

### Сортировка данных
- Нажмите на заголовок столбца для сортировки по возрастанию/убыванию

### Управление записями
- **Добавление**: нажмите кнопку "Добавить запись" и заполните форму
- **Редактирование**: нажмите на иконку редактирования в строке записи
- **Удаление**: нажмите на иконку удаления в строке записи (потребуется подтверждение)

## Структура проекта
```
DB_MySQL/
├── frontend/             # React приложение
│   ├── public/           # Статические файлы и HTML
│   └── src/              # Исходный код React
│       ├── components/   # React компоненты
│       │   └── MySQLTableViewer.jsx  # Основной компонент
│       ├── App.js        # Корневой компонент приложения
│       └── index.js      # Точка входа React приложения
│
└── backend/              # Python/Flask API
    ├── app.py            # Основной файл сервера и API-маршруты
    ├── requirements.txt  # Зависимости Python
    └── .env              # Файл конфигурации (не включен в репозиторий)
```

## API эндпоинты
- `GET /api/status` - проверка состояния сервера
- `GET /api/databases` - получить список баз данных
- `GET /api/tables` - получить список таблиц в базе данных
- `GET /api/tables/<table_name>/schema` - получить схему таблицы
- `GET /api/tables/<table_name>/data` - получить данные таблицы
- `POST /api/tables/<table_name>/add` - добавить запись
- `PUT /api/tables/<table_name>/update/<id>` - обновить запись
- `DELETE /api/tables/<table_name>/delete/<id>` - удалить запись

## Лицензия
Этот проект лицензируется под MIT License.

