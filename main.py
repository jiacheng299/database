from flask import Flask
from insert import insert_api
from update import update_api
from delete import delete_api
from search import search_api

app = Flask(__name__)
app.register_blueprint(insert_api)
app.register_blueprint(update_api)
app.register_blueprint(delete_api)
app.register_blueprint(search_api)
if __name__ == '__main__':
    app.run()