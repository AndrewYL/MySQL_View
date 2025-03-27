import os
import sys
import pathlib
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import traceback

# Явно указываем путь к файлу .env
env_path = pathlib.Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Создание экземпляра приложения Flask
app = Flask(__name__)
# Настраиваем CORS для разрешения запросов с любых источников
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Отладочная информация
print(f"Путь к файлу .env: {env_path}")
print(f"Файл .env существует: {os.path.exists(env_path)}")
print(f"Значения переменных окружения:")
print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
print(f"MYSQL_PASSWORD: {'*****' if os.getenv('MYSQL_PASSWORD') else 'Не задан'}")
print(f"MYSQL_DB: {os.getenv('MYSQL_DB')}")
print(f"MYSQL_PORT: {os.getenv('MYSQL_PORT')}")

# Проверяем наличие всех необходимых переменных окружения
required_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"Ошибка: Следующие переменные окружения не заданы: {', '.join(missing_vars)}")
    print("Пожалуйста, убедитесь, что файл .env содержит все необходимые переменные.")
    sys.exit(1)

try:
    # Создаем подключение к MySQL
    mysql_connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB'),
        port=int(os.getenv('MYSQL_PORT', '3306'))
    )
    print("Подключение к MySQL успешно установлено!")
except Exception as e:
    print(f"Ошибка при подключении к MySQL: {e}")
    traceback.print_exc()
    sys.exit(1)

# Вспомогательная функция для получения нового подключения к MySQL
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            port=int(os.getenv('MYSQL_PORT', '3306'))
        )
    except Exception as e:
        print(f"Ошибка при создании подключения к MySQL: {e}")
        traceback.print_exc()
        return None

# Определяем маршруты напрямую в файле app.py
@app.route('/')
def index():
    return jsonify({"message": "Welcome to MySQL API"})

@app.route('/api/databases', methods=['GET'])
def get_databases():
    try:
        print("Получение списка баз данных...")
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall() 
                    if db[0] not in ['information_schema', 'mysql', 'performance_schema', 'sys']]
        cursor.close()
        conn.close()
        
        print(f"Получено баз данных: {len(databases)}")
        return jsonify({"databases": databases})
    except Exception as e:
        print(f"Ошибка при получении списка баз данных: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/tables', methods=['GET'])
def list_tables():
    try:
        database = request.args.get('database')
        if database:
            print(f"Получение списка таблиц для БД: {database}")
            conn = get_db_connection()
            if not conn:
                return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
            
            cursor = conn.cursor()
            cursor.execute(f"USE `{database}`")
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            conn.close()
            return jsonify({"tables": tables})
        else:
            # По умолчанию используем базу данных из .env
            cursor = mysql_connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            cursor.close()
            
            # Преобразуем результат в список имен таблиц
            table_names = [table[0] for table in tables]
            
            return jsonify({"tables": table_names})
    except Exception as e:
        print(f"Ошибка при получении списка таблиц: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/tables/<table_name>/schema', methods=['GET'])
def get_table_schema(table_name):
    try:
        database = request.args.get('database')
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        if database:
            cursor.execute(f"USE `{database}`")
            
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        
        schema = []
        for column in columns:
            schema.append({
                "Field": column[0],
                "Type": column[1],
                "Null": column[2],
                "Key": column[3],
                "Default": column[4],
                "Extra": column[5]
            })
        
        return jsonify({"schema": schema})
    except Exception as e:
        print(f"Ошибка при получении схемы таблицы: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/tables/<table_name>/data', methods=['GET'])
def fetch_table_data(table_name):
    try:
        database = request.args.get('database')
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        if database:
            cursor.execute(f"USE `{database}`")
            
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        rows = cursor.fetchall()
        
        # Получаем имена столбцов
        cursor.execute(f"DESCRIBE {table_name}")
        columns_info = cursor.fetchall()
        column_names = [column[0] for column in columns_info]
        
        cursor.close()
        conn.close()
        
        # Преобразуем результат в список словарей
        result = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                row_dict[column_names[i]] = value
            result.append(row_dict)
        
        return jsonify({"data": result, "columns": column_names})
    except Exception as e:
        print(f"Ошибка при получении данных таблицы: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

# Дополнительная проверка состояния сервера и базы данных
@app.route('/api/status', methods=['GET'])
def check_status():
    try:
        # Проверяем подключение к БД
        conn = get_db_connection()
        if not conn:
            return jsonify({
                "status": "error",
                "message": "Не удалось подключиться к MySQL",
                "database": False
            }), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "ok",
            "message": "Сервер работает нормально",
            "database": True,
            "mysql_version": version[0] if version else "unknown"
        })
    except Exception as e:
        print(f"Ошибка при проверке статуса: {e}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e),
            "database": False
        }), 500

@app.route('/api/tables/<table_name>/add', methods=['POST'])
def add_record(table_name):
    try:
        data = request.get_json()
        database = data.get('database')
        record = data.get('record', {})
        
        if not record:
            return jsonify({"error": "Нет данных для добавления"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        if database:
            cursor.execute(f"USE `{database}`")
        
        # Формируем SQL запрос для вставки
        columns = ', '.join([f"`{col}`" for col in record.keys()])
        placeholders = ', '.join(['%s'] * len(record))
        values = list(record.values())
        
        query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        
        # Получаем ID добавленной записи
        last_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": "Запись успешно добавлена", 
            "id": last_id
        })
    except Exception as e:
        print(f"Ошибка при добавлении записи: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/tables/<table_name>/update/<int:record_id>', methods=['PUT'])
def update_record(table_name, record_id):
    try:
        data = request.get_json()
        database = data.get('database')
        record = data.get('record', {})
        id_column = data.get('id_column', 'id')  # Столбец для идентификации записи
        
        if not record:
            return jsonify({"error": "Нет данных для обновления"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        if database:
            cursor.execute(f"USE `{database}`")
        
        # Формируем SQL запрос для обновления
        set_clause = ', '.join([f"`{col}` = %s" for col in record.keys()])
        values = list(record.values())
        values.append(record_id)  # Добавляем ID для условия WHERE
        
        query = f"UPDATE `{table_name}` SET {set_clause} WHERE `{id_column}` = %s"
        cursor.execute(query, values)
        conn.commit()
        
        # Проверяем, была ли обновлена запись
        affected_rows = cursor.rowcount
        
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({
                "success": True, 
                "message": "Запись успешно обновлена"
            })
        else:
            return jsonify({
                "success": False, 
                "message": f"Запись с {id_column}={record_id} не найдена"
            }), 404
    except Exception as e:
        print(f"Ошибка при обновлении записи: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/tables/<table_name>/delete/<int:record_id>', methods=['DELETE'])
def delete_record(table_name, record_id):
    try:
        database = request.args.get('database')
        id_column = request.args.get('id_column', 'id')  # Столбец для идентификации записи
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        if database:
            cursor.execute(f"USE `{database}`")
        
        query = f"DELETE FROM `{table_name}` WHERE `{id_column}` = %s"
        cursor.execute(query, (record_id,))
        conn.commit()
        
        # Проверяем, была ли удалена запись
        affected_rows = cursor.rowcount
        
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({
                "success": True, 
                "message": "Запись успешно удалена"
            })
        else:
            return jsonify({
                "success": False, 
                "message": f"Запись с {id_column}={record_id} не найдена"
            }), 404
    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/tables/<table_name>/schema-details', methods=['GET'])
def get_table_schema_details(table_name):
    try:
        database = request.args.get('database')
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Не удалось подключиться к MySQL"}), 500
        
        cursor = conn.cursor()
        if database:
            cursor.execute(f"USE `{database}`")
            
        # Получаем детальную схему таблицы
        cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
        columns = cursor.fetchall()
        
        # Получаем информацию о первичных ключах
        cursor.execute(f"SHOW KEYS FROM `{table_name}` WHERE Key_name = 'PRIMARY'")
        primary_keys = [key[4] for key in cursor.fetchall()]  # 4 - Column_name в результате запроса
        
        cursor.close()
        conn.close()
        
        schema = []
        for column in columns:
            schema.append({
                "field": column[0],
                "type": column[1],
                "null": column[3],  # YES/NO
                "key": column[4],   # PRI/MUL/UNI
                "default": column[5],
                "extra": column[6],
                "comment": column[8] if len(column) > 8 else "",
                "isPrimary": column[0] in primary_keys,
                "isAutoIncrement": "auto_increment" in column[6].lower() if column[6] else False
            })
        
        return jsonify({"schema": schema})
    except Exception as e:
        print(f"Ошибка при получении детальной схемы таблицы: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)