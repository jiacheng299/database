from flask import Flask, jsonify, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import create
import model as Model

delete_api = Blueprint('delete_api', __name__)


@delete_api.route("/api/v1/<table_name>/<emp_no>/<dept_no>", methods=['DELETE'])
def delete_data1(table_name, emp_no, dept_no):
    if table_name in ['dept_emp', 'dept_manager']:
        if table_name == "dept_emp":
            model = create.Dept_emp
        elif table_name == "dept_manager":
            model = create.DeptManager
        obj = Model.session.query(model).filter_by(emp_no=emp_no, dept_no=dept_no).first()  # 提取并使用两个主键字段
        Model.session.delete(obj)
        Model.session.commit()
        return "'messages': 'record deleted successfully'", 204
    else:
        return 'Invalid table name', 400


@delete_api.route("/api/v1/<table_name>/<id>", methods=['DELETE'])
def delete_data2(table_name, id):
    if table_name in ["departments", "titles", "employees", "dept_manager_title"]:
        if table_name == "departments":
            model = create.Department
            obj = Model.session.query(model).filter_by(dept_no=id).first()
        elif table_name == "employees":
            model = create.Employee
            obj = Model.session.query(model).filter_by(emp_no=id).first()
        elif table_name == "dept_manager_title":
            model = create.DeptManagerTitle
            obj = Model.session.query(model).filter_by(emp_no=id).first()
        if not obj:
            return jsonify({'messages': 'record not found'}), 404
        Model.session.delete(obj)
        Model.session.commit()
        return jsonify({'messages': 'record deleted successfully'}), 204
    else:
        return 'Invalid table name', 400


@delete_api.route("/api/v1/<table_name>/<emp_no>/<title>/<from_data>", methods=['DELETE'])
def delete_data3(table_name, emp_no, title, from_data):
    if table_name == "titles":
        obj = Model.session.query(create.Title).filter_by(emp_no=emp_no, title=title, from_date=from_data).first()
        if not obj:
            return jsonify({'messages': 'record not found'}), 404
        Model.session.delete(obj)
        Model.session.commit()
        return jsonify({'messages': 'record deleted successfully'}), 204
    else:
        return 'Invalid table name', 400
