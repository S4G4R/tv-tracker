from flask import render_template, request, redirect, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
from app.models import User
from tv import db

app_routing = Blueprint('app_routing',__name__)

@app_routing.route('/')
@app_routing.route('/index')
def index():
    return render_template('index.html')

@app_routing.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        # TODO LOGIN LOGIC

        flash('Logged in successfully!')
        return redirect('/index')

    return render_template('login.html', form=form)

@app_routing.route('/register', methods=['GET','POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        pw_hash = generate_password_hash(form.password.data)

        username_present = User.query.filter_by(username=username).first()

        if username_present:
            flash('Username already registered!')
            return redirect('/index')

        new_user = User(username=username, pw_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully!')
        return redirect('/index')

    return render_template('register.html', form=form)
