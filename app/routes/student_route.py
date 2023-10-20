from flask import Blueprint, render_template, request
from app.models.student_models import student_model

student_bp = Blueprint('student_bp',__name__)

@student_bp.route('/students', methods=['GET', 'POST'])
def students():
    students = student_model.get_students()

    # Pass the retrieved data to the 'students.html' template
    return render_template("students.html", student_data=students)