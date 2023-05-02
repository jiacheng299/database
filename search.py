from flask import Flask, jsonify, request, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import create
import model as Model

search_api = Blueprint('search_api', __name__)


@search_api.route("/api/v1/<table_name>/<id>", methods=["GET"])
def get_one_record(table_name, id):
    if table_name in ["departments", "employees", "dept_manager_title"]:
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
            return jsonify({"message": "record not found"}), 404
        result = {}
        for column in obj.__table__.columns:
            result[column.name] = str(getattr(obj, column.name))
        return jsonify(result), 200
    else:
        return jsonify({"message": "Invalid table name"}), 400


@search_api.route("/api/v1/<table_name>/<emp_no>/<dept_no>", methods=['GET'])
def get_two_record(table_name, emp_no, dept_no):
    if table_name in ['dept_emp', 'dept_manager']:
        if table_name == "dept_emp":
            model = create.Dept_emp
        elif table_name == "dept_manager":
            model = create.DeptManager
        obj = Model.session.query(model).filter_by(emp_no=emp_no, dept_no=dept_no).first()  # 提取并使用两个主键字段
        result = {}
        for column in obj.__table__.columns:
            result[column.name] = str(getattr(obj, column.name))
        return jsonify(result), 200
    else:
        return 'Invalid table name', 400


@search_api.route("/api/v1/<table_name>/<emp_no>/<title>/<from_data>", methods=['GET'])
def get_three_record(table_name, emp_no, title, from_data):
    if table_name == "titles":
        obj = Model.session.query(create.Title).filter_by(emp_no=emp_no, title=title, from_date=from_data).first()
        if not obj:
            return jsonify({'messages': 'record not found'}), 404
        result = {}
        for column in obj.__table__.columns:
            result[column.name] = str(getattr(obj, column.name))
        return jsonify(result), 200
    else:
        return 'Invalid table name', 400


@search_api.route("/api/v1/<table_name>", methods=["GET"])
def get_records(table_name):
    # 根据路由参数判断需要查询的模型类
    model = None
    if table_name == "departments":
        model = create.Department
    elif table_name == "employees":
        model = create.Employee
    elif table_name == "dept_emp":
        model = create.Dept_emp
    elif table_name == "dept_manager":
        model = create.DeptManager
    elif table_name == "titles":
        model = create.Title
    # ... 其他模型类也可以在这里添加

    # 如果未找到模型类，则返回错误信息
    if not model:
        return jsonify({"message": "Invalid table name"}), 400

    # 解析查询字符串参数并构建查询条件
    args_dict = {}
    for name in request.args.keys():
        args_dict[name] = request.args.get(name)

    # 根据字典中的变量名和对应的值构造查询条件
    query_filters = []
    for name, value in args_dict.items():
        # 这里假设所有参数都是字符串类型
        query_filters.append(getattr(model, name) == value)

        # 执行查询并返回结果
    records = Model.session.query(model).filter(*query_filters).all()

    # 构建响应结果
    if not records:
        return jsonify({"message": "no records found"}), 404
    result = []
    for record in records:
        record_dict = {}
        for column in record.__table__.columns:
            record_dict[column.name] = str(getattr(record, column.name))
        result.append(record_dict)

    return jsonify(result), 200
