from flask import Blueprint, render_template

art_bp = Blueprint('art', __name__, url_prefix='/art')

@art_bp.route('/<int:art_id>')
def art_detail(art_id):
    return render_template('art_detail.html', art_id=art_id)
