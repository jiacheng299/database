from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:123456@localhost/test')
SessionFactory = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
session = SessionFactory(bind=engine)
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)