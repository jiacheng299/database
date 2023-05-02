from flask import Flask, jsonify, request,Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import create

import model as Model
insert_api = Blueprint('insert_api', __name__)
@insert_api.route("/api/v1/<table_name>", methods=['POST'])
def insert_data(table_name):
    data = request.get_json()

    if table_name in ["departments", "dept_emp", "dept_manager", "titles", "employees", "dept_manager_title"]:
        rows = data['rows']
        if table_name == "departments":
            model = create.Department
        elif table_name == "dept_emp":
            model = create.Dept_emp
        elif table_name == "dept_manager":
            model = create.DeptManager
        elif table_name == "titles":
            model = create.Title
        elif table_name == "employees":
            model = create.Employee
        elif table_name == "dept_manager_title":
            model = create.DeptManagerTitle
        row_dicts = [dict(row) for row in rows]
        Model.session.bulk_insert_mappings(model, row_dicts)
        Model.session.commit()
        return jsonify({'messages': f'{len(rows)} rows inserted into {table_name} successfully'}), 201
    else:
        return 'Invalid table name', 400

