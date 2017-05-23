from flask import render_template, flash, redirect, session, url_for, request
from app import app, db
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from models import User

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

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User succefully registred')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    return  redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
