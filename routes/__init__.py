from flask import Blueprint

home_bp = Blueprint('home', __name__)

def register_blueprints(app):
    from .home import home_bp as hb
    from .gallery import gallery_bp as gb
    from .art import art_bp as ab
    from .artist import artist_bp as arb
    from .cart import cart_bp as cb
    from .checkout import checkout_bp as cbp
    from .auth import auth_bp as authb
    from .account import account_bp as acb
    from .search import search_bp as sb
    from .info import info_bp as ib
    from .accessibility import accessibility_bp as acb2

    app.register_blueprint(hb)
    app.register_blueprint(gb)
    app.register_blueprint(ab)
    app.register_blueprint(arb)
    app.register_blueprint(cb)
    app.register_blueprint(cbp)
    app.register_blueprint(authb)
    app.register_blueprint(acb)
    app.register_blueprint(sb)
    app.register_blueprint(ib)
    app.register_blueprint(acb2)
