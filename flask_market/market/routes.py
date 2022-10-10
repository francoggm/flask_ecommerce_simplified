from flask import render_template, Blueprint, redirect, url_for, flash
from .models import Item, User
from . import db
from .forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
@login_required
def home_page():
    return render_template('home.html')

@routes.route('/market')
@login_required
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
            password=form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        flash('Successfuly registered!', category='success')
        login_user(user_to_create)
        return redirect(url_for('routes.home_page'))

    if form.errors:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('register.html', form=form)

@routes.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password_correction(attempted_password=form.password.data):
            login_user(user)
            flash('Success! You are logged', category='success')
            return redirect(url_for('routes.market_page'))
        flash('Username and password dont match, try again', category='danger')

    if form.errors:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('login.html', form=form)

@routes.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out!', category='info')
    return redirect(url_for('routes.home_page'))
    