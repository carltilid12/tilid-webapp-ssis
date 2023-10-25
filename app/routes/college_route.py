from flask import Blueprint, render_template, request, redirect, url_for, flash
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
            print('College created successfully', 'success')
        except Exception as e:
            print('Failed to create the college', 'error')
            error = 'Failed to create the college'

        return redirect(url_for('college_bp.colleges'))

    colleges = college_model.get_colleges()

    # Pass the retrieved data to the 'college.html' template
    return render_template("colleges.html", college_data=colleges)