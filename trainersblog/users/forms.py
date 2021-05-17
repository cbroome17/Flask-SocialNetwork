from trainersblog.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# flask_wtf FlaskForm - generalized form inheritance


class UserLoginForm(FlaskForm):
    """
    Creates the User Form for logging in a user
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UserRegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'confirm_pw', message='Passwords must match')])
    confirm_pw = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('That email has already been registered!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'That username already belongs to an account, try a different one!')


class UserUpdateForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('That email has already been registered!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'That username already belongs to an account, try a different one!')
