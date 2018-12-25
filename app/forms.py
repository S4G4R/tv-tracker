from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeatedPassword = PasswordField('Confirm Password', validators=[
                    DataRequired(),
                    EqualTo('password', message='Please enter the correct password!')])
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

class UpdateSeason(FlaskForm):
    show_id = HiddenField('', validators=[DataRequired()])
    season = IntegerField('Episodes')
    submit1 = SubmitField('⟳')

class AddEpisodes(FlaskForm):
    show_id = HiddenField('', validators=[DataRequired()])
    eps_watched = IntegerField('Episodes')
    submit2 = SubmitField('⟳')

class ChangeStatus(FlaskForm):
    movie_id = HiddenField('', validators=[DataRequired()])
    status = SelectField('Change Status', choices=[('Watched', 'Watched'), ('Not Watched', 'Not Watched')])
    submit1 = SubmitField('⟳')

class ChangeRating(FlaskForm):
    movie_id = HiddenField('', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[NumberRange(min=0,max=100,message='Enter rating between 0 and 100!')])
    submit2 = SubmitField('⟳')

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
