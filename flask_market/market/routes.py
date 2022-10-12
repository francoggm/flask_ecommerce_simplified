from flask import render_template, Blueprint, redirect, url_for, flash, request
from .models import Item, User
from . import db
from .forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, current_user, logout_user, login_required

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
@login_required
def home_page():
    return render_template('home.html')

@routes.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == 'POST':
        #Purchase item logic
        p_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name=p_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f'Congratulations, you purchased {p_item_obj.name} for {p_item_obj.price}$', category='success')
            else:
                flash(f'You dont have enought budget to buy {p_item_obj.name}, your budget is {current_user.budget}$', category='danger')

        #Sell item logic
        s_item = request.form.get('sell_item')
        s_item_obj = Item.query.filter_by(name=s_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f'Congratulations, you sold {s_item_obj.name} for {s_item_obj.price}$', category='success')
            else:
                flash(f"You can't sell {s_item_obj.name}, this item isn't in your account", category='danger')

        return redirect(url_for('routes.market_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, sell_form=sell_form,owned_items=owned_items)

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
    