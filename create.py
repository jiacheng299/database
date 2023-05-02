from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Index, Enum, DDL, event
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import model as Model

engine = create_engine('mysql+pymysql://root:123456@localhost/test')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class Department(Base):
    __tablename__ = 'departments'
    dept_no = Column(String(4), primary_key=True)
    dept_name = Column(String(40), nullable=False, unique=True)

    def __repr__(self):
        return f"<Title(dept_no={self.dept_no}, dept_name={self.dept_name})>"


class Dept_emp(Base):
    __tablename__ = 'dept_emp'
    emp_no = Column(Integer, ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True, nullable=False)
    dept_no = Column(String(4), ForeignKey('departments.dept_no', ondelete='CASCADE'), primary_key=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    dept_no_index = Index('dept_no', dept_no)
    employee = relationship('Employee', backref='dept_emp')
    department = relationship('Department', backref='dept_emp')


class DeptManager(Base):
    __tablename__ = 'dept_manager'
    emp_no = Column(Integer, ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    dept_no = Column(String(4), ForeignKey('departments.dept_no', ondelete='CASCADE'), primary_key=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    employee = relationship('Employee', backref='dept_manager')
    department = relationship('Department', backref='dept_manager')
    __table_args__ = (
        Index('dept_no', dept_no),
    )


class Title(Base):
    __tablename__ = 'titles'
    emp_no = Column(Integer, ForeignKey('employees.emp_no'), primary_key=True)
    title = Column(String(50), primary_key=True)
    from_date = Column(Date, primary_key=True)
    to_date = Column(Date)
    employee = relationship("Employee")

    def __repr__(self):
        return f"<Title(emp_no={self.emp_no}, title={self.title}, from_date={self.from_date}, to_date={self.to_date})>"


class Employee(Base):
    __tablename__ = 'employees'
    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(Enum('M', 'F'), nullable=False)
    hire_date = Column(Date, nullable=False)
    __table_args__ = (Index('ix_employees_first_name', 'first_name'),)

    def __repr__(self):
        return f"<Employee(emp_no={self.emp_no}, first_name={self.first_name}, last_name={self.last_name}, gender={self.gender}, birth_date={self.birth_date}, hire_date={self.hire_date})>"


class DeptManagerTitle(Base):
    __tablename__ = 'dept_manager_title'
    emp_no = Column(Integer, ForeignKey('employees.emp_no', ondelete='CASCADE'), primary_key=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    employee = relationship("Employee")

    def __repr__(self):
        return f"<DeptManagerTitle(emp_no={self.emp_no}, from_date={self.from_date}, to_date={self.to_date})>"


# 创建触发器的 DDL 语句
trigger_ddl1 = DDL("""
CREATE TRIGGER dept_manager_insert AFTER INSERT ON dept_manager
FOR EACH ROW
BEGIN
    INSERT INTO dept_manager_title (emp_no, from_date)
    VALUES (NEW.emp_no, NEW.from_date);
END
""")


# 注册触发器到数据库
@event.listens_for(DeptManager.__table__, 'after_create')
def after_create(target, connection, **kw):
    connection.execute(trigger_ddl1)


# 创建触发器的 DDL 语句
trigger_ddl2 = DDL("""
CREATE TRIGGER dept_manager_delete AFTER DELETE ON dept_manager
FOR EACH ROW
BEGIN
    DELETE FROM dept_manager_title
    WHERE emp_no = OLD.emp_no AND from_date = OLD.from_date;
END
""")


# 注册触发器到数据库
@event.listens_for(DeptManager.__table__, 'after_create')
def after_create(target, connection, **kw):
    connection.execute(trigger_ddl2)


if __name__ == '__main__':
    Base.metadata.create_all()
