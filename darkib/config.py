import os

basedir = os.path.abspath(os.path.dirname(__file__))

#Basic Flask settings
CSRF_ENABLED = True
SECRET_KEY = 'do not forget change it'

#Database 
#DB = dict(host='localhost', dbname='darkib', user='darkib_admin', password='its2forme')
SQLALCHEMY_DATABASE_URI = 'mysql://darkib_admin:its2forme@localhost/darkib'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
SQLALCHEMY_TRACK_MODIFICATIONS = False
