from flask import render_template, request, redirect
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():

    if request.method == "POST":
        # TODO
        return redirect('/')

    if request.method == "GET":
        form = LoginForm()
        return render_template('login.html', form=form)

@app.route('/register')
def register():

    if request.method == "POST":
        # TODO
        return redirect('/')

    if request.method == "GET":
        form = RegisterForm()
        return render_template('register.html', form=form)
