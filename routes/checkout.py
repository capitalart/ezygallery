from flask import Blueprint, render_template

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/')
def checkout():
    return render_template('checkout.html')
