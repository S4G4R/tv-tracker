from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeatedPassword = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class SearchForm(FlaskForm):
    type = SelectField('Choose one', choices=[
        ('tv', 'TV Show'),
        ('movie', 'Movie')
    ])
    title = StringField('Title Of TV Show/Movie', validators=[DataRequired()])
    submit = SubmitField('Search')

class QuickAddForm(FlaskForm):
    id = HiddenField('', validators=[DataRequired()])
    type = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('+ Quick Add')

class UpdateShow(FlaskForm):
    show_id = HiddenField('', validators=[DataRequired()])
    season = IntegerField('Episodes')
    eps_watched = IntegerField('Episodes')
    submit = SubmitField('⟳')

class UpdateMovie(FlaskForm):
    movie_id = HiddenField('', validators=[DataRequired()])
    status = SelectField('Change Status', choices=[('Watched', 'Watched'), ('Not Watched', 'Not Watched')])
    rating = IntegerField('Rating')
    submit = SubmitField('⟳')

class PasswordChangeForm(FlaskForm):
    old_pw = PasswordField('Old Password', validators=[DataRequired()])
    new_pw = PasswordField('New Password', validators=[DataRequired()])
    new_pw_again = PasswordField('New Password Again', validators=[
        DataRequired(),
        EqualTo('new_pw', message='Passwords do not match!')
    ])
    submit = SubmitField('Change Password')

class RemovalForm(FlaskForm):
    id = HiddenField('', validators=[DataRequired()])
    type = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('X')
