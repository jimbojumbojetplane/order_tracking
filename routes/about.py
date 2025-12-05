from flask import Blueprint, render_template
from auth import login_required

about_bp = Blueprint('about', __name__)

@about_bp.route('/about', methods=['GET'])
@login_required
def about():
    """About/Architecture page"""
    return render_template('about.html')

