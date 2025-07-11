from flask import Blueprint, render_template

artist_bp = Blueprint('artist', __name__, url_prefix='/artist')

@artist_bp.route('/<int:artist_id>')
def artist_profile(artist_id):
    return render_template('artist_profile.html', artist_id=artist_id)
