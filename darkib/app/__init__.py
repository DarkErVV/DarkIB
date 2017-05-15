from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')
#app.config.from_object('database_conf')

#Database initialisation
db = SQLAchemy(app)

from app import views, models
