from flask import render_template, request, redirect
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        return redirect('/index')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        return redirect('/index')

    return render_template('register.html', form=form)
