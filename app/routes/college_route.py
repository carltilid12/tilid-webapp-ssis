from flask import Blueprint, render_template, request
from app.models.college_models import college_model

college_bp = Blueprint('college_bp',__name__)

@college_bp.route('/colleges', methods=['GET', 'POST'])
def colleges():
    colleges = college_model.get_colleges()

    # Pass the retrieved data to the 'college.html' template
    return render_template("colleges.html", college_data=colleges)