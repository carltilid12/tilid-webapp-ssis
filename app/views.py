from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/students')
def students():
    return render_template("students.html")

@views.route('/courses')
def courses():
    return render_template("courses.html")

@views.route('/colleges')
def colleges():
    return render_template("colleges.html")
