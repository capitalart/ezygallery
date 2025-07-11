"""Robbie Mode™: EzyGallery minimal Flask app."""

"""Robbie Mode™: Imports"""
from flask import Flask, render_template

"""Robbie Mode™: App setup"""
app = Flask(__name__)

"""Robbie Mode™: Routes"""
@app.route('/')
def home():
    """Robbie Mode™: Home route"""
    return render_template('home.html')

@app.route('/gallery')
def gallery():
    """Robbie Mode™: Gallery route"""
    return render_template('gallery_page.html')

@app.route('/about')
def about():
    """Robbie Mode™: About route"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Robbie Mode™: Contact route"""
    return render_template('contact.html')

"""Robbie Mode™: App runner"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
