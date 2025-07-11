from flask import Blueprint, render_template, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.artwork import Artwork, Base

art_bp = Blueprint('art', __name__, url_prefix='/artwork')

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)

@art_bp.route('/<seo_filename>')
def artwork_detail(seo_filename):
    with Session() as session:
        artwork = session.query(Artwork).filter_by(seo_filename=seo_filename).first()
    if not artwork:
        abort(404)
    return render_template('artwork_detail.html', artwork=artwork)
