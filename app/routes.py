from flask import render_template, redirect, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from tv import db, login_manager

app_routing = Blueprint('app_routing',__name__)

@app_routing.route('/')
@app_routing.route('/index')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app_routing.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data

        username_present = User.query.filter_by(username=username).first()

        if not username_present:
            flash('Incorrect password or username!', 'error')
            return redirect('/index')

        current_user = username_present

        password = form.password.data
        pw_hash = username_present.pw_hash

        if not check_password_hash(pw_hash, password):
            flash('Incorrect password or username!', 'error')
            return redirect('/index')

        current_user.authenticated = True
        db.session.add(current_user)
        db.session.commit()

        login_user(current_user, remember=True)

        flash('Logged in successfully!', 'success')
        return redirect('/index')

    return render_template('login.html', form=form)

@app_routing.route('/logout', methods=['GET'])
@login_required
def logout():

    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()

    logout_user()

    flash('Logged out successfully!', 'success')

    return redirect('/index')

@app_routing.route('/register', methods=['GET','POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        pw_hash = generate_password_hash(form.password.data)

        username_present = User.query.filter_by(username=username).first()

        if username_present:
            flash('Username already registered!', 'error')
            return redirect('/index')

        new_user = User(username=username, pw_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully!', 'success')
        return redirect('/index')

    return render_template('register.html', form=form)
