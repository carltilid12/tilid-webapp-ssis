from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.student_models import student_model
from app.models.course_models import course_model

student_bp = Blueprint('student_bp',__name__)

@student_bp.route('/students', methods=['GET', 'POST'])
def students():
    error=None
    if request.method == 'POST':
        id = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        coursecode = request.form.get('course')
        studentyear = request.form.get('year')
        gender = request.form.get('gender')
        
        # Create a dictionary to hold the student data
        student_data = {
            'id': id,
            'firstname': firstname,
            'lastname': lastname,
            'coursecode': coursecode,
            'studentyear': studentyear,
            'gender': gender,
        }
        # Create the student by calling the model function
        try:
            student_model.create_student(student_data)
            error = None
            print('Student created successfully', 'success')
        except Exception as e:
            print('Failed to create the student', 'error')
            error = 'Failed to create the student'
            
        return redirect(url_for('student_bp.students'))
    
    courses = course_model.get_courses()
    students = student_model.get_students()

    # Pass the retrieved data to the 'students.html' template
    return render_template("students.html", student_data=students, course_data=courses, error=error)