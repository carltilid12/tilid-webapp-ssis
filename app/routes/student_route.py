from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
            flash('Student created successfully', 'success')
        except Exception as e:
            flash('Failed to create the student', 'error')
            error = 'Failed to create the student'
            
        return redirect(url_for('student_bp.students'))
    
    courses = course_model.get_courses()
    students = student_model.get_students()

    # Pass the retrieved data to the 'students.html' template
    return render_template("students.html", student_data=students, course_data=courses, error=error)

@student_bp.route('/update_student', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        # Get the updated student data from the form
        student_data = {
            'id': request.form.get('edit-id'),
            'firstname': request.form.get('edit-firstname'),
            'lastname': request.form.get('edit-lastname'),
            'coursecode': request.form.get('edit-course'),
            'studentyear': request.form.get('edit-year'),
            'gender': request.form.get('edit-gender')
        }

        try:
            # Call the update_student function to update the student in the database
            student_model.update_student(student_data)
            flash('Student updated successfully', 'success')
        except Exception as e:
            flash('Failed to update the student', 'error')

        # After updating, you can redirect to the students page or perform any other necessary actions
        return redirect(url_for('student_bp.students'))
    
@student_bp.route('/delete_student/<string:recordId>', methods=['DELETE'])
def delete_student(recordId):
    try:
        # Call the delete_student function from student_models.py
        success = student_model.delete_student(recordId)
        if success:
            return jsonify({'message': 'Student deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete student'})
    except Exception as e:
        return jsonify({'error': 'Failed to delete student'})