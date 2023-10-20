from flask import Blueprint, render_template, request
from app.models.course_models import course_model

course_bp = Blueprint('course_bp',__name__)

@course_bp.route('/courses', methods=['GET', 'POST'])
def courses():
    courses = course_model.get_courses()

    # Pass the retrieved data to the 'courses.html' template
    return render_template("courses.html", course_data=courses)