from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.student_models import student_model
from app.models.course_models import course_model
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from urllib.parse import urlparse
from werkzeug.utils import secure_filename

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
        file = request.form.get('file')
        cropped_image_data = request.form['croppedImageData']
        
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
            if file and (not cropped_image_data):
                flash('Invalid File Format', 'error')
                return redirect(url_for('student_bp.students'))
            elif not file:
                student_model.create_student(student_data)
                flash('Student created successfully', 'success')
            
            # Check if a file was provided
            if cropped_image_data:
                # Convert image data size from bytes to megabytes
                image_size_mb = len(cropped_image_data) / (1024 * 1024)

                # Check if the image size exceeds the limit
                if image_size_mb > 5:
                    flash(f'Image size exceeds the maximum limit of {5} MB', 'error')
                    return redirect(url_for('student_bp.students'))
                
                student_model.create_student(student_data)

                # Upload the file to Cloudinary
                oldimage = student_model.get_student_image_url(id)
                if oldimage:
                    parsed_url = urlparse(oldimage)
                    public_id = parsed_url.path.split("/")[-1].split(".")[0]
                    cloudinary.uploader.destroy(public_id)
                    print(public_id)

                upload_result = cloudinary.uploader.upload(cropped_image_data)
                image_url = upload_result['url']
                student_model.associate_image_url(image_url, id)

                flash('Student created successfully', 'success')

            error = None
        except Exception as e:
            flash('Failed to create the student', 'error')
            print(e)
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
        id = request.form.get('edit-id')
        file = request.form.get('edit-file')
        cropped_image_data = request.form['croppedImageData']

        try:
            if file and (not cropped_image_data):
                flash('Invalid File Format', 'error')
                return redirect(url_for('student_bp.students'))
            elif not file:
                student_model.update_student(student_data)
                flash('Student updated successfully', 'success')
            # Check if a file was provided
            elif cropped_image_data:
                
                # Convert image data size from bytes to megabytes
                image_size_mb = len(cropped_image_data) / (1024 * 1024)

                # Check if the image size exceeds the limit
                if image_size_mb > 5:
                    flash(f'Image size exceeds the maximum limit of {5} MB', 'error')
                    return redirect(url_for('student_bp.students'))
                
                student_model.update_student(student_data)
                
                # Upload the file to Cloudinary
                oldimage = student_model.get_student_image_url(id)
                if oldimage:
                    parsed_url = urlparse(oldimage)
                    public_id = parsed_url.path.split("/")[-1].split(".")[0]
                    cloudinary.uploader.destroy(public_id)
                    print(public_id)

                upload_result = cloudinary.uploader.upload(cropped_image_data)
                image_url = upload_result['url']
                student_model.associate_image_url(image_url, id)

                flash('Student updated successfully', 'success')

        except Exception as e:
            flash('Failed to update the student', 'error')

        # After updating, you can redirect to the students page or perform any other necessary actions
        return redirect(url_for('student_bp.students'))
    
@student_bp.route('/delete_student/<string:recordId>', methods=['DELETE'])
def delete_student(recordId):
    try:
        # Call the delete_student function from student_models.py
        oldimage = student_model.get_student_image_url(recordId)
        if oldimage:
            parsed_url = urlparse(oldimage)
            public_id = parsed_url.path.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)
            print(public_id)

        success = student_model.delete_student(recordId)
        if success:
            return jsonify({'message': 'Student deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete student'})
    except Exception as e:
        return jsonify({'error': 'Failed to delete student'})
    
@student_bp.route('/student/<string:student_id>', methods=['GET'])
def view_student(student_id):
    try:
        # Fetch the details of the student based on the student ID
        student_details = student_model.get_student_by_id(student_id)
        if student_details:
            # Render the student details page with the retrieved data
            return render_template("student_details.html", student_details=student_details)
        else:
            flash('Student not found', 'error')
            return redirect(url_for('student_bp.students'))

    except Exception as e:
        print(e)
        flash('Failed to retrieve student details', 'error')
        return redirect(url_for('student_bp.students'))

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@student_bp.route('/student/upload-image', methods=['POST'])
def upload_image():
    try:
        # Assuming you have a form with an input field named 'file'
        student_id = request.form['student_id']
        cropped_image_data = request.form['croppedImageData']

        # Check if a file was provided
        if cropped_image_data:
            # Convert image data size from bytes to megabytes
            image_size_mb = len(cropped_image_data) / (1024 * 1024)

            # Check if the image size exceeds the limit
            if image_size_mb > 5:
                flash(f'Image size exceeds the maximum limit of {5} MB', 'error')
                return redirect(url_for('student_bp.view_student', student_id=student_id))
            
            # Check if the file extension is allowed
            filename = secure_filename(request.files['file'].filename)
            if not allowed_file(filename):
                flash(f'Invalid file extension. Allowed extensions are: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
                return redirect(url_for('student_bp.view_student', student_id=student_id))
            
            # Upload the file to Cloudinary
            oldimage = student_model.get_student_image_url(student_id)
            if oldimage:
                parsed_url = urlparse(oldimage)
                public_id = parsed_url.path.split("/")[-1].split(".")[0]
                cloudinary.uploader.destroy(public_id)
                print(public_id)

            upload_result = cloudinary.uploader.upload(cropped_image_data)
            image_url = upload_result['url']
            student_model.associate_image_url(image_url, student_id)
            flash('Image uploaded successfully', 'success')
            return redirect(url_for('student_bp.view_student', student_id=student_id))
        else:
            flash('No or Invalid File detected', 'error')
            return redirect(url_for('student_bp.view_student', student_id=student_id))

    except Exception as e:
        flash('Failed to upload image', 'error')
        print(str(e))  # Log the exception for debugging

    return redirect(url_for('student_bp.students'))