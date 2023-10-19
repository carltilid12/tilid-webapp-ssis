from flask import Blueprint, render_template
from app import mysql

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/students')
def students():
    connection = mysql.connection
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM student')
    data = cursor.fetchall()
    cursor.close()

    # Pass the retrieved data to the 'students.html' template
    return render_template("students.html", student_data=data)

@views.route('/courses')
def courses():
    connection = mysql.connection
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM course')
    data = cursor.fetchall()
    cursor.close()

    # Pass the retrieved data to the 'courses.html' template
    return render_template("courses.html", course_data=data)

@views.route('/colleges')
def colleges():
    connection = mysql.connection
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM college')
    data = cursor.fetchall()
    cursor.close()

    # Pass the retrieved data to the 'courses.html' template
    return render_template("colleges.html", college_data=data)
