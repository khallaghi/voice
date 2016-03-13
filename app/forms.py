from wtforms import Form, BooleanField, TextField, PasswordField,SelectField, RadioField,validators
class FacultyForm(Form):
	name = TextField('Faculty name', [validators.Length(min=4, max=25)])
	uni = SelectField('University')

class ProfessorForm(Form):
	name = TextField('Professor name', [validators.Length(min=2, max=100)])
	family = TextField('Professor family', [validators.Length(min=2, max=100)])
	email = TextField('Email address')
	website = TextField('website')
	faculty = RadioField(' faculty ',coerce=unicode)
	room_no = TextField('room number')
	rank = RadioField('rank')
	# uni = SelectField('University')
class SearchForm(Form):
	search = TextField('search it')
class RateForm(Form):
	

	