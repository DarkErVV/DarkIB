#Basic Flask settings
CSRF_ENABLED = True
SECRET_KEY = 'do not forget change it'

#Database 
SQLALCHEMY_DATABASE_URI = ('mysql://%s:%s@%s/%s?charset=utf8') % ( app.config['DB']['user'],
                                                                   app.config['DB']['password'],
                                                                   app.config['DB']['host'],
                                                                   app.config['DB']['dbname'])
