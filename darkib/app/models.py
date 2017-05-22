from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id    = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(255))
    email = db.Column(db.String(255))
    paswd_hash = db.Column(db.String(40))

    def __repr__(self):
        return '<User %r>' % (self.nickname)
