from flask import render_template, redirect, Blueprint, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, SearchForm, QuickAddForm, AddEpisodes, UpdateSeason, ChangeStatus, ChangeRating, PasswordChangeForm
from app.models import User, Show, Movie
from app.search import search_movie, search_tv, search_by_id
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

    if current_user.is_authenticated:
        return redirect('/index')

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data

        username_present = User.query.filter_by(username=username).first()

        if not username_present:
            flash('Incorrect password or username!', 'error')
            return redirect('/login')

        password = form.password.data
        pw_hash = username_present.pw_hash

        if not check_password_hash(pw_hash, password):
            flash('Incorrect password or username!', 'error')
            return redirect('/login')

        username_present.authenticated = True
        db.session.add(username_present)
        db.session.commit()

        login_user(username_present, remember=True)

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

    if current_user.is_authenticated:
        return redirect('/index')

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        pw_hash = generate_password_hash(form.password.data)

        username_present = User.query.filter_by(username=username).first()

        if username_present:
            flash('Username already registered!', 'error')
            return redirect('/register')

        new_user = User(username=username, pw_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully!', 'success')
        return redirect('/index')

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

    seasonform = UpdateSeason()
    episodeform = AddEpisodes()

    if seasonform.submit1.data and seasonform.validate_on_submit():
        id = seasonform.show_id.data
        season = seasonform.season.data

        show = db.session.query(Show).filter_by(show_id=id).first()

        show.curr_season = season

        db.session.commit()

        flash('Updated successfully!', 'success')
        return redirect('/shows')

    if episodeform.submit2.data and episodeform.validate_on_submit():
        id = episodeform.show_id.data
        eps = episodeform.eps_watched.data

        show = db.session.query(Show).filter_by(show_id=id).first()

        show.eps_watched = eps

        db.session.commit()

        flash('Updated successfully!', 'success')
        return redirect('/shows')

    return render_template('shows.html', shows=shows, episodeform=episodeform, seasonform=seasonform)

@app_routing.route('/movies', methods=['GET','POST'])
@login_required
def movies():

    movies = Movie.query.filter_by(user_id=current_user.id).all()

    changestatus = ChangeStatus()
    changerating = ChangeRating()

    if changestatus.submit1.data and changestatus.validate_on_submit():
        id = changestatus.movie_id.data
        status = changestatus.status.data

        movie = db.session.query(Movie).filter_by(movie_id=id).first()

        movie.status = status

        db.session.commit()

        flash('Updated successfully!', 'success')
        return redirect('/movies')

    if changerating.submit2.data and changerating.validate_on_submit():
        id = changerating.movie_id.data
        rating = changerating.rating.data

        movie = db.session.query(Movie).filter_by(movie_id=id).first()

        movie.rating = rating

        db.session.commit()

        flash('Updated successfully!', 'success')
        return redirect('/movies')

    return render_template('movies.html', movies=movies, changestatus=changestatus, changerating=changerating)

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
