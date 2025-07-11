from flask import Blueprint, render_template

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
def cart():
    return render_template('cart.html')
