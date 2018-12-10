from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeatedPassword = PasswordField('Confirm Password', validators=[
                                        DataRequired(),
                                        EqualTo('password', message='Please enter the correct password!')
                                                                    ]
                                    )
    submit = SubmitField('Register')
