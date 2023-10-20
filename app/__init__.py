from flask import Flask
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect

mysql = MySQL()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        #BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )

    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)

    from .views import views
    from .routes.student_route import student_bp
    from .routes.course_route import course_bp
    from .routes.college_route import college_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(student_bp, url_prefix='/')
    app.register_blueprint(course_bp, url_prefix='/')
    app.register_blueprint(college_bp, url_prefix='/')
    return app
