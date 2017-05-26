from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    username  = db.Column('username', db.String(20))
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50))
    registred_on = db.Column('registred_on', db.DateTime)
    images = db.relationship('Images', backref='author', lazy='dynamic')

    def __init__( self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registred_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Images(db.Model):
    id =  db.Column( db.Integer, primary_key = True) 
    md5_hash = db.Column( db.String(40) )
    height = db.Column( db.Integer )
    weight = db.Column( db.Integer )
    type = db.Column( db.Integer )
    date_upload = db.Column( db.DateTime )
    user_id = db.Column( db.Integer, db.ForeignKey('user.user_id') )

    def __init__(self, md5_hash, h, w, im_type, user_id):
        self.md5_hash = md5_hash
        self.user_id = user_id
        self.height = h
        self.weight = w
        self.type = im_type
        self.date_upload = datetime.utcnow()

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Img MD5: %r>' % (self.body)
