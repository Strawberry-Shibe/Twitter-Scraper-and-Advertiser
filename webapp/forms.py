from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp


class LoginForm(FlaskForm):
	"""
	super basic login form

	Attributes
		- self.form_type : Hidden
			attribute to help the backend distinguish between input and registration forms on one page
		- self.email : String
			email input field. backend also allows for username to be used here instead
		- self.password : Password
			password input field.
		- self.submit : Submit
			button with which to submit the form.
	"""
	# super basic login form
	form_type = HiddenField()  # flag for identifying what form has been submitted when 2 forms are on one page
	email = StringField('Email', validators=[DataRequired()])  # doesnt have email validator as username can also be used
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login', false_values=[False])


class RegistrationForm(FlaskForm):
	"""
	registration form, needs work to implement access token for managing authorised sign ups
	and add password complexity requirements

	Attributes
		- self.form_type : Hidden
			attribute to help the backend distinguish between input and registration forms on one page
		- self.username : String
			username input field. required, minimum length of 3, maximum length of 15
		- self.email : String
			email input. required, must be email
		- self.password : Password
			password input. required
		- self.confirm_password : Password
			password confirmation input. required, input must match self.password
		- self.submit : Submit
			button with which to submit the form.
	"""
	# TODO implement access token for managing authorised sign ups
	# TODO add password complexity requirements
	form_type = HiddenField()  # flag for identifying what form has been submitted when 2 forms are on one page
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register', false_values=[False])

