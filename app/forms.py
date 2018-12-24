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
