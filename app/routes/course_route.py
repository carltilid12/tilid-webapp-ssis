from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.models.course_models import course_model
from app.models.college_models import college_model

course_bp = Blueprint('course_bp',__name__)

@course_bp.route('/courses', methods=['GET', 'POST'])
def courses():
    error = None
    if request.method == 'POST':
        coursecode = request.form.get('code')
        coursename = request.form.get('name')
        collegecode = request.form.get('college')

        # Create a dictionary to hold the course data
        course_data = {
            'coursecode': coursecode,
            'coursename': coursename,
            'collegecode': collegecode,
        }

        # Create the course by calling the model function
        try:
            course_model.create_course(course_data)
            error = None
            print('Course created successfully', 'success')
        except Exception as e:
            print('Failed to create the course', 'error')
            error = 'Failed to create the course'

        return redirect(url_for('course_bp.courses'))
    
    courses = course_model.get_courses()
    colleges = college_model.get_colleges()

    # Pass the retrieved data to the 'courses.html' template
    return render_template("courses.html", course_data=courses, college_data=colleges)