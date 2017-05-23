from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return  render_template("index.html")

@app.route('/new')
def new_img():
    return  render_template("new_img.html")

@app.route('/about')
def about():
    return render_template('about.html')
