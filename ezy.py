from flask import Flask
from routes.gallery import gallery_bp
from routes.marketplace import marketplace_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py', silent=True)

# Register blueprints
app.register_blueprint(gallery_bp)
app.register_blueprint(marketplace_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
