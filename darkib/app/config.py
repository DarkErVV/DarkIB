
#Basic Flask settings
CSRF_ENABLED = True
SECRET_KEY = 'do not forget change it'

#Database 
#DB = dict(host='localhost', dbname='darkib', user='darkib_admin', password='its2forme')
SQLALCHEMY_DATABASE_URI = ('mysql://%s:%s@%s/%s?charset=utf8') % ( 'localhost',
                                                                   'darkib',
                                                                   'darkib_admin',
                                                                   'its2forme')
