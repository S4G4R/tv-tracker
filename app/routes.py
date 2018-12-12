from flask import render_template, request, redirect, Blueprint, flash
from app.forms import LoginForm, RegisterForm

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

        # TODO REGISTER LOGIC

        flash('Registered successfully!')
        return redirect('/index')

    return render_template('register.html', form=form)
