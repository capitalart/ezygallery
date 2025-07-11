from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

@gallery_bp.route('/')
def gallery():
    return render_template('gallery.html')
