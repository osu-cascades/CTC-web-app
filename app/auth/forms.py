from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me', default=False)
	submit = SubmitField('Login')


class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, numbers, dots or underscores')])
	first_name = StringField('First Name', validators=[Required(), Length(3, 64)])
	last_name = StringField('Last Name', validators=[Required(), Length(3, 64)])
	password = PasswordField('Password', validators=[Required(), Length(12, 64, message='Password must be at least 12 characters long'), 
											EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


class ChangePasswordForm(Form):
	old_password = PasswordField('Old password', validators=[Required()])
	password = PasswordField('New password', validators=[Required(), Length(12, 64, message='Password must be atleast 12 characters long'),
												EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm new password', validators=[Required()])
	submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Reset Password')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
	email = StringField('New Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Update Email Address')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')
