from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')
#app.config.from_object('database_conf')

db = SQLAchemy(app)

from app import views, models
