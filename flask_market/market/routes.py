from flask import render_template, Blueprint, redirect, url_for, flash
from .models import Item, User
from . import db
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

@routes.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data, 
            email=form.email.data,
            password_hash=form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('routes.market_page'))

    if form.errors:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('register.html', form=form)