from flask import render_template, Blueprint
from .models import Item
from .forms import RegisterForm

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
def home_page():
    return render_template('home.html')

@routes.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@routes.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)