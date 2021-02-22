from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class SignUpForm(FlaskForm):
    fullName = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password',
                                                                                             message='Both password '
                                                                                                     'fields much '
                                                                                                     'match')])
    signUp = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField('Login')


class EditForm(FlaskForm):
    name = StringField("Pet's Name:", validators=[InputRequired()])
    age = StringField("Pet's Age:",validators=[InputRequired()])
    bio = StringField("Pet's Bio:",validators=[InputRequired()])
    edit = SubmitField('Edit Pet',validators=[InputRequired()])
