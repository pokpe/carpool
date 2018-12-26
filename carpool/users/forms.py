from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.widgets import Input
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from carpool.models import User
from carpool.settings import Settings

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),
                                        Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])

    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Account with that email already exist')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TextOutput(Input):
    def __call__(self, field, **kwargs):
        return kwargs.get('value', field._value())

class ROTextField(StringField):
    widget = TextOutput()

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),
                                        Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])

    week_day = SelectField('Drive day', choices=Settings.week_days_array)

    car_points = ROTextField('Drive points')

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Account with that email already exist')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email. Register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
