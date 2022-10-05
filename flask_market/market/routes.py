from flask import render_template, Blueprint
from .models import Item

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home_page():
    return render_template('home.html')

@views.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)