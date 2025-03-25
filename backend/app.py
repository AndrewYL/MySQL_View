from flask import Flask, render_template, request
from flask_cors import CORS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)

# Замените на свои параметры подключения
DB_URL = 'mysql+pymysql://user:password@localhost/database'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def get_tables():
    """Получение списка таблиц"""
    with engine.connect() as connection:
        tables = connection.execute(text("SHOW TABLES")).fetchall()
        return [table[0] for table in tables]


def get_table_data(table_name, limit=10, offset=0):
    """Получение данных таблицы"""
    session = Session()
    try:
        query = text(f"SELECT * FROM {table_name} LIMIT :limit OFFSET :offset")
        result = session.execute(query, {'limit': limit, 'offset': offset})

        columns = result.keys()
        data = [dict(zip(columns, row)) for row in result.fetchall()]
        return list(columns), data
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении данных: {str(e)}")
    finally:
        session.close()


@app.route('/')
def index():
    """Главная страница со списком таблиц"""
    tables = get_tables()
    return render_template('index.html', tables=tables)


@app.route('/table/<table_name>')
def view_table(table_name):
    """Просмотр конкретной таблицы"""
    tables = get_tables()
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit

    try:
        columns, data = get_table_data(table_name, limit, offset)
        total_rows = engine.connect().execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        total_pages = (total_rows + limit - 1) // limit

        return render_template('table.html',
                               tables=tables,
                               current_table=table_name,
                               columns=columns,
                               data=data,
                               current_page=page,
                               total_pages=total_pages)
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)