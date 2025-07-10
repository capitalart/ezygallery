from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth')

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
