from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def create_db(db):
    if not 'market.db' in os.listdir(os.getcwd()):
        db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ecf9db4de02eb105a1713893'
db = SQLAlchemy(app)
create_db(db)

from .routes import routes

app.register_blueprint(routes, url_prefix='/')




