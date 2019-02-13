from tv import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    pw_hash = db.Column(db.String(80), nullable=False)
    movies = db.relationship('Movie', backref='user')
    shows = db.relationship('Show', backref='user')

class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Not Watched')
    rating = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(80), nullable=False)
    curr_season = db.Column(db.Integer, default=1)
    eps_watched = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
