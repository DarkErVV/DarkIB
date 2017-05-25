from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm 
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from models import User

@app.route('/')
@app.route('/index')
def index():
    user = g.user
    return  render_template("index.html", user=user )

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

    #Get data from request
    username = request.form['username']
    password = request.form['password']

    #Database Query
    registered_user = User.query.filter_by(username=username, password=password).first()

    #User is not present in database
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))

    login_user(registered_user)
    flash('Logged in successfully')

    return  redirect(request.args.get(next) or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
