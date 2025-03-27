from sqlalchemy import create_engine, inspect, text, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Определение моделей на основе таблиц из базы данных
class Employees(Base):
    __tablename__ = 'employees'
    
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    hire_date = Column(Date)
    position = Column(String(100))
    
    # Связи
    department = relationship("Departments", back_populates="employees")
    passport = relationship("Passport", back_populates="employee", uselist=False)
    education = relationship("Education", back_populates="employee")
    children = relationship("Children", back_populates="employee")
    payments = relationship("Payments", back_populates="employee")

class Departments(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))
    
    # Связи
    employees = relationship("Employees", back_populates="department")

class Passport(Base):
    __tablename__ = 'passport'
    
    passport_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    series = Column(String(10))
    number = Column(String(20))
    issue_date = Column(Date)
    
    # Связи
    employee = relationship("Employees", back_populates="passport")

class Education(Base):
    __tablename__ = 'education'
    
    education_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    institution = Column(String(200))
    degree = Column(String(100))
    graduation_year = Column(Integer)
    
    # Связи
    employee = relationship("Employees", back_populates="education")

class Children(Base):
    __tablename__ = 'children'
    
    child_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    first_name = Column(String(50))
    birth_date = Column(Date)
    
    # Связи
    employee = relationship("Employees", back_populates="children")

class Payments(Base):
    __tablename__ = 'payments'
    
    payment_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    payment_date = Column(Date)
    amount = Column(Float)
    
    # Связи
    employee = relationship("Employees", back_populates="payments")

class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        # Связываем модели с базой данных
        Base.metadata.create_all(self.engine)

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