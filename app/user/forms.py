from wtforms import Form, BooleanField, TextField, PasswordField, SelectField,\
RadioField,validators, IntegerField
from flask_wtf.file import FileField

class ProfessorForm(Form):
	name = TextField('Professor name', [validators.Length(min=2, max=100)])
	# family = TextField('Professor family', [validators.Length(min=2, max=100)])
	email = TextField('Email address')
	website = TextField('website')
	faculty = RadioField(' faculty ',coerce=unicode)
	room_no = TextField('room number')
	rank = RadioField('rank')
	pic = FileField('Image File')
	# uni = SelectField('University')
