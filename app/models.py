from tv import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    pw_hash = db.Column(db.String(80), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    movies = db.relationship('Movie', backref='user')
    shows = db.relationship('Show', backref='user')

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return self.authenticated

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(80), nullable=False)
    curr_season = db.Column(db.Integer, default=1)
    eps_watched = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
