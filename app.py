from flask import Flask, url_for
from datetime import datetime
from routes import register_blueprints
import config

app = Flask(__name__)
app.config.from_object(config.Config)
register_blueprints(app)

@app.context_processor
def cache_buster():
    def static_url(filename):
        if app.config.get('FORCE_NOCACHE'):
            version = int(datetime.utcnow().timestamp())
            return url_for('static', filename=filename, v=version)
        return url_for('static', filename=filename)
    return dict(static_url=static_url)

@app.route('/toggle-nocache')
def toggle_nocache():
    app.config['FORCE_NOCACHE'] = not app.config.get('FORCE_NOCACHE', False)
    return f"FORCE_NOCACHE = {app.config['FORCE_NOCACHE']}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
