from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from app import app, db, lm
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from models import User, Images
from werkzeug.utils import secure_filename
from os import path, makedirs, getcwd, remove
from hashlib import md5
from PIL import Image
import tempfile
import shutil

from  sqlalchemy.sql.expression import func


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    img_last = Images.query.order_by("id desc").limit(3).all()
    img_rand = Images.query.order_by(func.rand()).limit(3).all()
    return render_template("index.html", img_last=img_last, img_rand=img_rand, user=user, content_title="Main Page.")


@app.route('/new')
def new_img():
    img = Images.query.order_by("id desc").limit(20).all()

    return render_template("new_img.html", img=img, content_title="New Images.")


@app.route('/about')
def about():
    return render_template('about.html', content_title="About.")


@app.route('/register', methods=['GET', 'POST'])
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

    # Get data from request
    username = request.form['username']
    password = request.form['password']

    # Database Query
    registered_user = User.query.filter_by(username=username, password=password).first()

    # User is not present in database
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))

    login_user(registered_user)
    flash('Logged in successfully')

    return redirect(request.args.get(next) or url_for('index'))

@app.route('/img/<md5_hash>')
def view_img(md5_hash):
    img = Images.query.filter_by(md5_hash=md5_hash).first()
    if img is None:
        flash('Image not found.')
        return redirect(url_for('new'))
    
    return render_template('img_view.html', img=img, content_title="Image Information.")

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


# Upload
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
            flash('No selected file!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Get secure filename
            sec_fname = path.join(app.config['TEMP_FOLDER'], secure_filename(file.filename))
            file.save(sec_fname)

            # Calculating MD5 hash and use it as filename
            md5_hash = calc_md5(sec_fname)
            save_dir = path.join(app.config['UPLOAD_FOLDER'], md5_hash[0:3])
            if not path.exists(save_dir):
                makedirs(save_dir)
            # copy to new dir
            save_path = path.join(save_dir, md5_hash)
            shutil.copy2(sec_fname, save_path)
            # remove temp
            remove(sec_fname)

            # Get resolution of image
            im = Image.open(save_path)

            im_type = 0  # default Image type

            if im.format == 'JPEG':
                im_type = 0
            elif im.format == 'PNG':
                im_type = 1
            elif im.format == 'GIF':
                im_type = 2

            original_size = im.size

            # Image thumbnail
            thumbs_dir = path.join(app.config['THUMBNAIL_FOLDER'], md5_hash[0:3])

            if not path.exists(thumbs_dir):
                makedirs(thumbs_dir)

            save_path = path.join(thumbs_dir, md5_hash)
            try:
                im.thumbnail((200,200), Image.ANTIALIAS )
                im.save(save_path, "JPEG")
            except IOError:
                print("cannot create thumbnail")

            img = Images(md5_hash, original_size[1], original_size[0], im.size[1], im.size[0], im_type, g.user.id)
            db.session.add(img)
            db.session.commit()

            flash('File successfully uploaded. MD5: ' + md5_hash)
            return redirect(url_for('index'))

    return render_template('upload.html')


@app.route('/thumbs/<filename>')
def send_thumbs(filename):
    root_dir = path.dirname(getcwd())
    send_dir = path.join(root_dir, 'darkib', app.config['THUMBNAIL_FOLDER'], filename[0:3])

    return send_from_directory(send_dir, filename, mimetype='image/jpeg')


@app.route('/file/<filename>')
def send_file(filename):
    root_dir = path.dirname(getcwd())
    send_dir = path.join(root_dir, 'darkib', app.config['UPLOAD_FOLDER'], filename[0:3])
    print(root_dir,send_dir,filename)
    return send_from_directory(send_dir, filename, mimetype='image')


def calc_md5(fname):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

