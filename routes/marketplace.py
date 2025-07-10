from flask import Blueprint, render_template

marketplace_bp = Blueprint('marketplace_bp', __name__, template_folder='../templates/marketplace')

@marketplace_bp.route('/marketplace')
def marketplace_home():
    return render_template('marketplace/marketplace_home.html')
