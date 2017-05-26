from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from app import app, db, lm
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from models import User, Images
from werkzeug.utils import secure_filename
from os import path
from hashlib import md5

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

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))

    return render_template('user.html', user=g.user)

#Upload
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #calculating MD5 Hash and use it as filename
            md5_hash = calc_md5(file)

            save_path = path.join(app.config['UPLOAD_FOLDER'], md5_hash)
            file.save(save_path)

            flash('File succefuly uploaded. MD5: ' + md5_hash )
            return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def calc_md5(fname):
    hash_md5 = md5()
    for chunk in iter(lambda: fname.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()
