from flask import Flask, jsonify, request, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import create
import model as Model

update_api = Blueprint('update_api', __name__)


@update_api.route("/api/v1/<table_name>", methods=['PUT'])
def update_data(table_name):
    row = request.get_json()
    if table_name == "departments":
        dept = Model.session.query(create.Department).filter_by(dept_no=row['dept_no']).first()
        if dept:
            dept.dept_name = row['dept_name']
            Model.session.commit()
            return jsonify({'messages': 'update successfully'}), 201
        else:
            return jsonify({'messages': 'department does not exist'}), 404

    if table_name == "dept_emp":
        dept_emp = Model.session.query(create.Dept_emp).filter_by(emp_no=row['emp_no'], dept_no=row['dept_no']).first()
        if dept_emp:
            dept_emp.from_date = row['from_date']
            dept_emp.to_date = row['to_date']
            Model.session.commit()
            return jsonify({'messages': 'update successfully'}), 201
        else:
            return jsonify({'messages': 'employee is not in department'}), 404

    if table_name == "dept_manager":
        dept_manager = Model.session.query(create.DeptManager).filter_by(emp_no=row['emp_no'],
                                                                         dept_no=row['dept_no']).first()
        if dept_manager:
            dept_manager.from_date = row['from_date']
            dept_manager.to_date = row['to_date']
            Model.session.commit()
            return jsonify({'messages': 'update successfully'}), 201
        else:
            return jsonify({'messages': 'employee is not a manager of department'}), 404

    if table_name == "titles":
        title = Model.session.query(create.Title).filter_by(emp_no=row['emp_no'], title=row['title'],
                                                            from_date=row['from_date']).first()
        if title:
            title.to_date = row['to_date']
            Model.session.commit()
            return jsonify({'messages': 'update successfully'}), 201
        else:
            return jsonify({'messages': 'employee does not have this title'}), 404

    if table_name == "employees":
        emp = Model.session.query(create.Employee).filter_by(emp_no=row['emp_no']).first()
        if emp:
            emp.birth_date = row['birth_date']
            emp.first_name = row['first_name']
            emp.last_name = row['last_name']
            emp.gender = row['gender']
            emp.hire_date = row['hire_date']
            Model.session.commit()
            return jsonify({'messages': 'update successfully'}), 201
        else:
            return jsonify({'messages': 'employee does not exist'}), 404
