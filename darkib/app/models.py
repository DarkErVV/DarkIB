from app import db
from datetime import datetime
 

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    username  = db.Column('username', db.String(20))
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50))
    registred_on = db.Column('registred_on', db.DateTime)

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

