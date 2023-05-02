from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import create
import model as Model
import csv

data_mapping = {
    "departments": create.Department,
    "dept_emp": create.Dept_emp,
    "dept_manager": create.DeptManager,
    "titles": create.Title,
    "employees": create.Employee,
    "dept_manager_title": create.DeptManagerTitle
}


# 读取csv数据集
def read_csv_to_db(file_path, table_name):
    with open(file_path, newline='') as csvfile:
        # 以字典形式读取
        reader = csv.DictReader(csvfile)
        rows = [dict(row) for row in reader]
        model = data_mapping[table_name]
        Model.session.bulk_insert_mappings(model, rows)
        Model.session.commit()


def main():
    # 插入departments.csv数据
    read_csv_to_db('../departments.csv', 'departments')
    # 插入employees.csv数据
    read_csv_to_db('../employees.csv', 'employees')
    # 插入dept_emp.csv数据
    read_csv_to_db('../dept_emp.csv', 'dept_emp')
    # 插入dept_manager.csv数据
    read_csv_to_db('../dept_manager.csv', 'dept_manager')
    # 插入titles.csv数据
    read_csv_to_db('../titles.csv', 'titles')


if __name__ == '__main__':
    main()
