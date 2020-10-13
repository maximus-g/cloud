import os
from datetime import datetime
from werkzeug.security import (generate_password_hash,
check_password_hash)
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_login import UserMixin
from cloud import app, db, login
from cloud.config import Config


admin = Admin(app, name="Cloud", template_mode="bootstrap3")



class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), unique=False, nullable=False)
	last_name = db.Column(db.String(20), unique=False, nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	password_hash = db.Column(db.String(128)) 

	# Relationships
	audios = db.relationship('Audio', backref='user', lazy='dynamic')
	documents = db.relationship('Document', backref='user', lazy='dynamic')
	images = db.relationship('Image', backref='user', lazy='dynamic')
	videos = db.relationship('Video', backref='user', lazy='dynamic')
    

	@property
	def password(self):
		''' Raise an error whenever there's an attempt to read the password '''
		raise AttributeError('Password is not a readable attribute')

	@password.setter
	def password(self, password):
		''' Generate password hash '''
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		'''Check whether the entered password matches the hash'''
		return check_password_hash(self.password_hash, password)


class Audio(db.Model):
	''' Contain '.mp3' and other audio files. '''
	__tablename__ = 'audios'
	id      	= db.Column(db.Integer, primary_key=True)
	name   = db.Column(db.String(100), unique=False, default='Untitled')
	content    	= db.Column(db.LargeBinary)
	date    	= db.Column(db.DateTime, default=datetime.utcnow)
	user_id 	= db.Column(db.Integer,db.ForeignKey('users.id'),
	nullable='False' )

class Document(db.Model):
	''' Contains '.txt', '.pdf', '.docx' etc files. ''' 
	__tablename__ = 'documents'
	id      	= db.Column(db.Integer, primary_key=True)
	name   = db.Column(db.String(100), unique=False, default='Untitled')
	content    	= db.Column(db.LargeBinary)
	date    	= db.Column(db.DateTime, default=datetime.utcnow)
	user_id 	= db.Column(db.Integer,db.ForeignKey('users.id'),
	nullable='False' )

class Image(db.Model):
	''' Contains '.png', ',jpeg', '.jpg' etc files. '''
	__tablename__ = 'images'
	id      	= db.Column(db.Integer, primary_key=True)
	name   = db.Column(db.String(100), unique=False, default='Untitled')
	content    	= db.Column(db.LargeBinary)
	date    	= db.Column(db.DateTime, default=datetime.utcnow)
	user_id 	= db.Column(db.Integer,db.ForeignKey('users.id'),
	nullable='False' )

class Video(db.Model):
	''' Contains '.mp4', '.mkv' etc files. '''
	__tablename__ = 'videos'
	id      	= db.Column(db.Integer, primary_key=True)
	name   = db.Column(db.String(100), unique=False, default='Untitled')
	content    	= db.Column(db.LargeBinary)
	date    	= db.Column(db.DateTime, default=datetime.utcnow)
	user_id 	= db.Column(db.Integer,db.ForeignKey('users.id'),
	nullable='False' )


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

admin.add_view(ModelView(User, db.session))
