from flask import Blueprint, render_template

accessibility_bp = Blueprint('accessibility', __name__)

@accessibility_bp.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')
