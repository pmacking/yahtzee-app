from flask_wtf import FlaskForm
# below classes are utilized for picture data and picture validation in forms
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
# below wtforms classes enable various attributes in form classes
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# below wtforms.validators validate form fields
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from yahtzee.models import User


class RegistrationForm(FlaskForm):
    """
    This is the registration form class utilized in /register route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    # add attributes set to imported wtforms classes
    # included args '<Titlecase>' html label
    # add args as imported wtforms.validators classes with sub args as req
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First Name',
                             validators=[DataRequired(),
                                         Length(min=1, max=25)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(),
                                        Length(min=1, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Validates username before add/commit user in route

        :param username: username of form.
        """
        user = User.query.filter_by(username=username.data).first()
        # if username exists, throw error
        if user:
            raise ValidationError(f'Please select a unique username.')

    def validate_email(self, email):
        """
        Validates email before add/commit user in route

        :param email: email of form.
        """
        user = User.query.filter_by(email=email.data).first()
        # if email exists, throw error
        if user:
            raise ValidationError(f'Please select a unique email.')


class LoginForm(FlaskForm):
    """
    This is the login form utilized in /login route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    # add attributes set to imported wtforms classes
    # included args '<Titlecase>' html label
    # add args as imported wtforms.validators classes with sub args as req
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    This is the update account form class utilized in /account route

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First Name',
                             validators=[DataRequired(),
                                         Length(min=1, max=25)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(),
                                        Length(min=1, max=25)])
    picture = FileField(
                'Profile Picture',
                validators=[FileAllowed(['jpg', 'png'])]
                )
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validates username before add/commit user in route

        :param username: username in form.
        """
        # first check if user is updating username before validating unique
        if username.data != current_user.username:

            # validate uniqueness of username
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'Please select a unique username.')

    def validate_email(self, email):
        """Validates email before add/commit user in route

        :param email: email of form.
        """
        # first check if user is updating email before validating unique
        if email.data != current_user.email:

            # validate uniqueness of email
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'Please select a unique email.')


class RequestResetForm(FlaskForm):
    """
    This is a form to request a password reset token

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """
        Validate email doesn't exist so we can inform user to create account.

        :param email: email of form.
        """
        # check if email exists, otherwise they can't request reset
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f'Email does not exist, please register.')


class ResetPasswordForm(FlaskForm):
    """
    This is a form to reset password

    :param FlaskForm: class inheretence from FlaskForm in flask_wtf
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')
