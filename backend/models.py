from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_tables(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def get_table_data(self, table_name, limit=10, offset=0):
        session = self.Session()
        try:
            # Запрос с поддержкой лимита и смещения
            query = text(f"SELECT * FROM {table_name} LIMIT :limit OFFSET :offset")
            result = session.execute(query, {'limit': limit, 'offset': offset})

            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            return {"columns": list(columns), "data": data}
        except Exception as e:
            raise RuntimeError(f"Ошибка при получении данных: {str(e)}")
        finally:
            session.close()