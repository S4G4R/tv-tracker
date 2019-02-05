from flask import render_template, redirect, Blueprint, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, SearchForm, QuickAddForm, PasswordChangeForm, RemovalForm, UpdateShow, UpdateMovie
from app.models import User, Show, Movie
from app.search import search_movie, search_tv, search_by_id
from flask_login import login_user, logout_user, login_required, current_user
from tv import db, login_manager

app_routing = Blueprint('app_routing',__name__)

@login_manager.user_loader
def load_user(id):
    """
    Returns a User instance when an id is provided.
    This function is required by the flask_login package.
    """
    return User.query.get(id)

@app_routing.route('/')
@app_routing.route('/index')
def index():
    """
    Goes to homepage.
    """
    return render_template('index.html')

@app_routing.route('/login', methods=['GET','POST'])
def login():
    """
    Logs a user in.
    """
    # If the user is currently authenticated already, just redirect to homepage.
    if current_user.is_authenticated:
        return redirect('/index')

    # Generate the login form
    form = LoginForm()

    # If the user has submitted a POST request, it will be validated below.
    if form.validate_on_submit():

        # Store the inputted username
        username = form.username.data

        # Check if the user exists
        user = User.query.filter_by(username=username).first()

        # If the user does not exist, show error and redirect to login page.
        if not user:
            flash('Incorrect password or username!', 'error')
            return redirect('/login')

        # Store password and retrive the password hash stored in the database.
        password = form.password.data
        pw_hash = user.pw_hash

        # If the two are not equal, show error and redirect to login page.
        if not check_password_hash(pw_hash, password):
            flash('Incorrect password or username!', 'error')
            return redirect('/login')

        # Authenticate the user
        user.authenticated = True
        db.session.add(user)
        db.session.commit()

        # Actually login the user through flask_login
        login_user(user, remember=True)

        # Show success message and redirect back to homepage.
        flash('Logged in successfully!', 'success')
        return redirect('/index')

    # If the request was GET, render the login page with the login form.
    return render_template('login.html', form=form)

@app_routing.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Logs a user out.
    """

    # De-authenticate the current user.
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()

    # Log user out.
    logout_user()

    # Show success message and redirect back to homepage.
    flash('Logged out successfully!', 'success')
    return redirect('/index')

@app_routing.route('/register', methods=['GET','POST'])
def register():
    """
    Registers a new user.
    """
    # If the user is currently authenticated already, just redirect to homepage.
    if current_user.is_authenticated:
        return redirect('/index')

    # Generate the form
    form = RegisterForm()

    # If the user has submitted a POST request, it will be validated below.
    if form.validate_on_submit():

        # Store the username and generate a password hash from the provided password
        username = form.username.data
        pw_hash = generate_password_hash(form.password.data)

        # Check if the username is already registered
        user = User.query.filter_by(username=username).first()

        # If so, show error and redirect to register page
        if user:
            flash('Username already registered!', 'error')
            return redirect('/register')

        # Create a new user, and add to the database
        new_user = User(username=username, pw_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        # Show success message and redirect to homepage
        flash('Registered successfully!', 'success')
        return redirect('/index')

    # If the request was GET, render the register page with the registration form.
    return render_template('register.html', form=form)

@app_routing.route('/myaccount', methods=['GET'])
@login_required
def myaccount():

    username = current_user.username

    return render_template('account.html', username=username)

@app_routing.route('/search', methods=['GET','POST'])
@login_required
def search():

    form = SearchForm()

    if form.validate_on_submit():

        form_title = form.title.data
        form_type = form.type.data

        if form_type == 'tv':
            results = search_tv(form_title)
        else :
            results = search_movie(form_title)

        form = QuickAddForm()
        return render_template('results.html',results=results,type=form_type,form=form)

    return render_template('search.html', form=form)

@app_routing.route('/quickadd', methods=['POST'])
@login_required
def quickadd():

    id = request.form.get('id')
    type = request.form.get('type')

    result = search_by_id(id, type)

    if type == 'tv':
        show_present = Show.query.filter_by(show_id=id).first()

        if show_present:
            flash('Show already in your list!', 'error')
            return redirect('/index')

        new_show = Show(
            show_id = result['id'],
            show_name = result['name'],
            user_id = current_user.id
        )

        db.session.add(new_show)
        db.session.commit()

        flash('Added show successfully!', 'success')

    else :
        movie_present = Movie.query.filter_by(movie_id=id).first()

        if movie_present:
            flash('Movie already in your list!', 'error')
            return redirect('/index')

        new_movie = Movie(
            movie_id = result['id'],
            movie_name = result['title'],
            user_id = current_user.id
        )

        db.session.add(new_movie)
        db.session.commit()

        flash('Added movie successfully!', 'success')

    return redirect('/index')

@app_routing.route('/shows', methods=['GET','POST'])
@login_required
def shows():

    shows = Show.query.filter_by(user_id=current_user.id).all()

    updateshow = UpdateShow()
    removal = RemovalForm()

    if updateshow.validate_on_submit():
        id = updateshow.show_id.data
        season = updateshow.season.data
        eps = updateshow.eps_watched.data

        show = db.session.query(Show).filter_by(show_id=id).first()
        show.curr_season = season
        show.eps_watched = eps

        db.session.commit()

        flash('Updated successfully!', 'success')
        return redirect('/shows')

    return render_template('shows.html', shows=shows, updateshow=updateshow, removal=removal)

@app_routing.route('/movies', methods=['GET','POST'])
@login_required
def movies():

    movies = Movie.query.filter_by(user_id=current_user.id).all()

    updatemovie = UpdateMovie()
    removal = RemovalForm()

    if updatemovie.validate_on_submit():
        id = updatemovie.movie_id.data
        status = updatemovie.status.data
        rating = updatemovie.rating.data

        if rating < 0 or rating > 100:
            flash('Please enter a rating between 0 and 100!', 'error')
            return redirect('/movies')

        movie = db.session.query(Movie).filter_by(movie_id=id).first()

        movie.status = status
        movie.rating = rating

        db.session.commit()

        flash('Updated successfully!', 'success')
        return redirect('/movies')

    return render_template('movies.html', movies=movies, updatemovie=updatemovie, removal=removal)

@app_routing.route('/changepassword', methods=['GET','POST'])
@login_required
def changepassword():

    form = PasswordChangeForm()

    if form.validate_on_submit():

        old_pw = form.old_pw.data
        new_pw = form.new_pw.data

        curr_pw_hash = db.session.query(User).filter_by(id=current_user.id).first().pw_hash

        if not check_password_hash(curr_pw_hash, old_pw):
            flash('Wrong password! Please try again.','error')
            return redirect('/changepassword')

        user = db.session.query(User).filter_by(id=current_user.id).first()

        user.pw_hash = generate_password_hash(new_pw)

        db.session.commit()

        flash('Changed successfully!', 'success')
        return redirect('/myaccount')

    return render_template('change_password.html', form=form)

@app_routing.route('/remove', methods=['POST'])
@login_required
def remove():

    id = request.form.get('id')
    type = request.form.get('type')

    if type == 'tv':
        result = db.session.query(Show).filter_by(show_id=id).first()
    else :
        result = db.session.query(Movie).filter_by(movie_id=id).first()

    db.session.delete(result)
    db.session.commit()

    if type == 'tv':
        flash('Show deleted successfully!', 'success')
        return redirect('/shows')
    else :
        flash('Movie deleted successfully!', 'success')
        return redirect('/movies')
