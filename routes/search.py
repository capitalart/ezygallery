from flask import Blueprint, render_template

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/')
def search():
    return render_template('search.html')
