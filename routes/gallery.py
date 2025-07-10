from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery_bp', __name__, template_folder='../templates/gallery')

@gallery_bp.route('/')
def gallery_home():
    return render_template('gallery/gallery_home.html')
