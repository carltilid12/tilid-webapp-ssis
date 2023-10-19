from flask import Flask
from flask_mysql_connector import MySQL

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hoshino'

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    return app