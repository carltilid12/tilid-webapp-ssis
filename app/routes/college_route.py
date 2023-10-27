from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.college_models import college_model

college_bp = Blueprint('college_bp',__name__)

@college_bp.route('/colleges', methods=['GET', 'POST'])
def colleges():
    if request.method == 'POST':
        collegecode = request.form.get('collegecode')
        collegename = request.form.get('collegename')

        # Create a dictionary to hold the college data
        college_data = {
            'collegecode': collegecode,
            'collegename': collegename,
        }

        # Create the college by calling the model function
        try:
            college_model.create_college(college_data)
            error = None
            flash('College created successfully', 'success')
        except Exception as e:
            flash('Failed to create the college', 'error')
            error = 'Failed to create the college'

        return redirect(url_for('college_bp.colleges'))

    colleges = college_model.get_colleges()

    # Pass the retrieved data to the 'college.html' template
    return render_template("colleges.html", college_data=colleges)

@college_bp.route('/update_college', methods=['GET', 'POST'])
def update_college():
    if request.method == 'POST':
        # Get the updated college data from the form
        college_data = {
            'collegecode': request.form.get('edit-collegecode'),
            'collegename': request.form.get('edit-collegename')
        }

        try:
            # Call the update_college function to update the college in the database
            college_model.update_college(college_data)
            flash('College updated successfully', 'success')
        except Exception as e:
            flash('Failed to update the college', 'error')

        # After updating, you can redirect to the colleges page or perform any other necessary actions
        return redirect(url_for('college_bp.colleges'))

@college_bp.route('/delete_college/<string:collegecode>', methods=['DELETE'])
def delete_college(collegecode):
    try:
        # Call the delete_college function from college_models.py
        success = college_model.delete_college(collegecode)
        if success:
            return jsonify({'message': 'College deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete college'})
    except Exception as e:
        return jsonify({'error': 'Failed to delete college'})



