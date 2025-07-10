from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin')
def admin_home():
    return render_template('admin/admin_home.html')
