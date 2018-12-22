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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    overview = db.Column(db.String(1000))

class Show(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    overview = db.Column(db.String(1000))
