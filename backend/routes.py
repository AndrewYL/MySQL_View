from app import app, db
from models import Employees, Departments, Passport, Education, Children, Payments
from flask import jsonify

# Словарь моделей для удобства
MODELS = {
    'Employees': Employees,
    'Departments': Departments,
    'Passport': Passport,
    'Education': Education,
    'Children': Children,
    'Payments': Payments
}

@app.route('/api/mysql/tables', methods=['GET'])
def get_tables():
    tables = list(MODELS.keys())
    return jsonify({'tables': tables})


@app.route('/api/mysql/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    """Получение данных конкретной таблицы"""
    try:
        # Проверяем существование модели
        if table_name not in MODELS:
            return jsonify({'error': 'Таблица не найдена'}), 404

        # Получаем модель
        model = MODELS[table_name]

        # Получаем колонки
        columns = [column.name for column in model.__table__.columns]

        # Получаем данные с лимитом
        results = model.query.limit(1000).all()

        # Преобразуем результаты в список словарей
        data = []
        for row in results:
            row_dict = {}
            for column in columns:
                value = getattr(row, column)
                # Преобразуем даты и другие специфичные типы в строки
                if hasattr(value, 'isoformat'):
                    row_dict[column] = value.isoformat()
                elif value is None:
                    row_dict[column] = 'NULL'
                else:
                    row_dict[column] = str(value)
            data.append(row_dict)

        return jsonify({
            'columns': columns,
            'rows': data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mysql/relations', methods=['GET'])
def get_table_relations():
    """Получение связей между таблицами"""
    relations = [
        {'table': 'Passport', 'column': 'employee_id', 'referenced_table': 'Employees',
         'referenced_column': 'employee_id'},
        {'table': 'Education', 'column': 'employee_id', 'referenced_table': 'Employees',
         'referenced_column': 'employee_id'},
        {'table': 'Children', 'column': 'employee_id', 'referenced_table': 'Employees',
         'referenced_column': 'employee_id'},
        {'table': 'Payments', 'column': 'employee_id', 'referenced_table': 'Employees',
         'referenced_column': 'employee_id'},
        {'table': 'Employees', 'column': 'department_id', 'referenced_table': 'Departments',
         'referenced_column': 'department_id'}
    ]
    return jsonify({'relations': relations})