from flask_login import UserMixin
from webapp import db
from werkzeug.security import generate_password_hash, check_password_hash


class PersistentStorage(db.Model):
	"""
	Database table for storing random values needed in the backend

	Attributes
		- self.id : str - (16 chars)
			database id string
		- self.content: str - (long text)
			data associated with the id
	"""
	#
	id = db.Column(db.String(32), primary_key=True)
	content = db.Column(db.Text)

	def __repr__(self):
		return f"PersistentStorage('{self.id}','{self.content}')"


class User(UserMixin, db.Model):
	"""
	Database table for storing login user information

	Attributes
		- self.id : str - (16 chars)
			user id string
		- self.username : str - (16 chars)
		- self.email : str - (255 chars)
		- self.password_hash : str - (255 chars)
		- self.password : str - (255 chars)
		- self.role : str - (16 chars)

	Methods
		- verify_password : compares the hash of the input password to the stored password hash
	"""
	id = db.Column(db.String(16), primary_key=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	password = db.Column(db.String(255), nullable=False)
	role = db.Column(db.String(16))

	def __repr__(self):
		return f"User('{self.id}','{self.username}', '{self.email}', '{self.role}'"

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


class post_collection(db.Model):
	"""
	Database table for storing cleaned post data

	Attributes
		- self.postID : str - (45 chars)
			Twitter,Flickr's post id
		- self.posterID : str - (45 chars)
			poster's id
		- self.postContent : str - (255 chars)
			content of the post
		- self.postDateTime : DateTime
			post time
		- self.longitude : float
			post location's longitude
		- self.latitude : float
			post location's latitude
		- self.sentiment : str - (10 chars)
			post's sentiment
		- self.manager : str - (45 chars)
	"""

	_tablename_: str = 'post_collection'

	post_id = db.Column(db.String(45), primary_key=True)
	poster_id = db.Column(db.String(45), nullable=False)
	post_content = db.Column(db.Text, nullable=False)
	post_date_time = db.Column(db.DateTime, nullable=False)
	platform = db.Column(db.String(10), nullable=False)
	longitude = db.Column(db.Float, nullable=False)
	latitude = db.Column(db.Float, nullable=False)
	sentiment = db.Column(db.Float, nullable=False)
	keyword = db.Column(db.String(32), nullable=False)

	def __repr__(self):
		return f"post_collection('{self.post_id}','{self.poster_id}','{self.post_date_time}','{self.sentiment}')"


class external_user(db.Model):
	"""
	Database table for storing social media users

	Attributes
		- self.user_id : str - (45 chars)
		- self.user_name : str - (45 chars)
		- self.verified : TINYINT(1) - Boolean
		- self.account_creation_date : date
		- self.post_frequency : DateTime
		- self.account_weight : float
		- self.confirmed_bot : float
	"""

	_tablename_ = 'external_user'

	user_id = db.Column(db.String(45), primary_key=True)
	user_name = db.Column(db.String(45), nullable=False)
	verified = db.Column(db.Boolean, nullable=False)
	account_creation_date = db.Column(db.Date, nullable=False)
	post_frequency = db.Column(db.Integer, nullable=False)
	account_weight = db.Column(db.Float, nullable=False)
	confirmed_bot = db.Column(db.Boolean, nullable=False)

	def __repr__(self):
		return f"external_user('{self.user_id}','{self.user_name}','{self.verified}','{self.account_creation_date}')"