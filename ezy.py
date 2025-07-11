# =============================================================================
#  EzyGallery.com — Main Flask App Entrypoint (ezy.py)
#  Robbie Mode™ — Best Practice, Production-Ready, Cache-Busted, Modular
#  Version: 2025-07-11
#
#  Instructions:
#   - Place this file at your project root.
#   - All static assets and templates use cache-busting for instant updates.
#   - Blueprints: Add new modules/routes under /routes/ and /templates/
#   - All major sections below are commented for easy navigation.
# =============================================================================

import os
from flask import Flask, url_for

# === 1. Flask App Setup ===
app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py', silent=True)

# === 2. Static Asset Cache-Busting (Best Practice) ===
def dated_url_for(endpoint, **values):
    """
    Appends ?v=file_mtime to static asset URLs for cache-busting.
    Ensures every new asset version is always reloaded.
    """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            static_folder = os.path.join(app.root_path, 'static')
            file_path = os.path.join(static_folder, filename)
            if os.path.isfile(file_path):
                values['v'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
app.context_processor(lambda: dict(url_for=dated_url_for))

# === 3. Register Blueprints ===
from routes.gallery import gallery_bp
from routes.marketplace import marketplace_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

# Optional (create these files/routes as needed)
try:
    from routes.home import home_bp
    app.register_blueprint(home_bp)
except ImportError:
    pass

try:
    from routes.uploads import uploads_bp
    app.register_blueprint(uploads_bp)
except ImportError:
    pass

try:
    from routes.docs import docs_bp
    app.register_blueprint(docs_bp)
except ImportError:
    pass

# Core routes
app.register_blueprint(gallery_bp)
app.register_blueprint(marketplace_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# === 4. Global No-Cache Headers (to fix dev cache issues) ===
@app.after_request
def add_no_cache_headers(response):
    """
    Add headers to disable browser and proxy caching of all pages and static files.
    """
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# === 5. Healthcheck Endpoint (for uptime monitors, Docker, etc) ===
@app.route("/health")
def health():
    return "OK", 200

# === 6. App Entrypoint ===
if __name__ == "__main__":
    # Set to port 8001, debug ON for dev. Use gunicorn for production!
    app.run(host="0.0.0.0", port=8080, debug=True)

# =============================================================================
#  Developer Quick Tips:
#   - Always use {{ url_for('static', filename='...') }} for CSS/JS/images!
#   - Add new blueprints as needed.
#   - "CTRL+F5" or "CMD+SHIFT+R" for a real hard refresh.
#   - Use dev-refresh.sh to quickly kill/restart Flask and clean caches (optional).
#   - For questions, check the Robbie Mode™ cheat-sheet. 😉
# =============================================================================
