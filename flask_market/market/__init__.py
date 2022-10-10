from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

def create_db(db):
    if not 'market.db' in os.listdir(os.getcwd()):
        db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ecf9db4de02eb105a1713893'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'routes.login_page'
login_manager.login_message_category = 'info'

from .routes import routes
app.register_blueprint(routes, url_prefix='/')

from .models import User, Item
create_db(db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






