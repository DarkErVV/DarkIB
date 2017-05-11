DB = dict(host='localhost', dbname='darkib', user='darkib_admin', password='its2forme')

SQLALCHEMY_DATABASE_URI = ('mysql://%s:%s@%s/%s?charset=utf8') % ( DB['user'],
                                                                   DB['password'],
                                                                   DB['host'],
                                                                   DB['dbname'])
