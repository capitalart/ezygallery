#!/bin/bash
set -e

# ---- Make Folders ----
cd ~
mkdir -p ezygallery/{routes,scripts,logs,tests}
mkdir -p ezygallery/static/{css,js,images,icons,fonts}
mkdir -p ezygallery/templates/{components,admin,auth,gallery,marketplace}

cd ezygallery
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip flask

# ---- Requirements ----
pip freeze > requirements.txt

# ---- .gitignore ----
cat <<EOL > .gitignore
venv/
__pycache__/
*.pyc
.env
logs/
EOL

# ---- .env ----
cat <<EOL > .env
FLASK_ENV=development
SECRET_KEY=$(openssl rand -hex 16)
EOL

# ---- README.md ----
echo "# EzyGallery.com — Digital Art Marketplace" > README.md

# ---- config.py ----
cat <<EOL > config.py
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changeme'
EOL

# ---- Placeholder CSS files ----
cat <<EOL > static/css/base.css
body { font-family: sans-serif; background: #faf9f6; margin:0; padding:0;}
EOL
touch static/css/components.css static/css/layout.css static/css/theme.css static/css/sidebar.css

# ---- Placeholder JS ----
touch static/js/base.js

# ---- Placeholder templates ----
# main.html with nav
cat <<'EOL' > templates/main.html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{% block title %}EzyGallery.com{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/layout.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/sidebar.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('gallery_bp.gallery_home') }}">Gallery</a> |
        <a href="{{ url_for('marketplace_bp.marketplace_home') }}">Marketplace</a> |
        <a href="{{ url_for('auth_bp.login') }}">Login</a> |
        <a href="{{ url_for('admin_bp.admin_home') }}">Admin</a>
    </nav>
    <div id="main-content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
EOL

# ---- Section templates ----
cat <<EOL > templates/gallery/gallery_home.html
{% extends "main.html" %}
{% block title %}Gallery — EzyGallery.com{% endblock %}
{% block content %}
<h1>Gallery</h1>
<p>This is the Gallery section. (Placeholder)</p>
{% endblock %}
EOL

cat <<EOL > templates/marketplace/marketplace_home.html
{% extends "main.html" %}
{% block title %}Marketplace — EzyGallery.com{% endblock %}
{% block content %}
<h1>Marketplace</h1>
<p>This is the Marketplace section. (Placeholder)</p>
{% endblock %}
EOL

cat <<EOL > templates/auth/login.html
{% extends "main.html" %}
{% block title %}Login — EzyGallery.com{% endblock %}
{% block content %}
<h1>Login</h1>
<p>Login form coming soon!</p>
{% endblock %}
EOL

cat <<EOL > templates/admin/admin_home.html
{% extends "main.html" %}
{% block title %}Admin — EzyGallery.com{% endblock %}
{% block content %}
<h1>Admin Dashboard</h1>
<p>Admin section placeholder.</p>
{% endblock %}
EOL

cat <<EOL > templates/components/header.html
<!-- Header component (you can {% include %} this anywhere) -->
<header><h2>EzyGallery Header</h2></header>
EOL

# ---- Blueprints in routes/ ----
cat <<EOL > routes/gallery.py
from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery_bp', __name__, template_folder='../templates/gallery')

@gallery_bp.route('/')
def gallery_home():
    return render_template('gallery/gallery_home.html')
EOL

cat <<EOL > routes/marketplace.py
from flask import Blueprint, render_template

marketplace_bp = Blueprint('marketplace_bp', __name__, template_folder='../templates/marketplace')

@marketplace_bp.route('/marketplace')
def marketplace_home():
    return render_template('marketplace/marketplace_home.html')
EOL

cat <<EOL > routes/auth.py
from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth')

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
EOL

cat <<EOL > routes/admin.py
from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin')
def admin_home():
    return render_template('admin/admin_home.html')
EOL

# ---- Main app ezy.py ----
cat <<EOL > ezy.py
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
EOL

echo "✅ EzyGallery project structure created with modular routes, templates, CSS, and nav!"
echo "1. cd ~/ezygallery"
echo "2. source venv/bin/activate"
echo "3. python ezy.py"
echo "4. Visit http://localhost:8001/ (Gallery), /marketplace, /login, /admin"

