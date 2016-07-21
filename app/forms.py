from wtforms import Form, BooleanField, TextField, PasswordField, SelectField,\
RadioField,validators, IntegerField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
# from flaskext.uploads import UploadSet, IMAGES
class UniversityForm(Form):
	name = TextField('University name', validators=[DataRequired()])
	
class FacultyForm(Form):
	name = TextField('Faculty name', validators=[DataRequired()])
	uni = SelectField('University')
	# pic = FileField('ImageField')

class ProfForm(Form):
	name = TextField('Professor name', validators=[DataRequired()])
	email = TextField('Email address', validators=[DataRequired()])
	website = TextField('website')
	uni = SelectField('university', coerce=unicode, choices = [])
	# faculty = SelectField('faculty', choices = [] )
	room_no = TextField('room number')
	rank = SelectField('rank')
	pic = FileField('Image File')

class ProfForFacForm(Form):
	name = TextField('Professor name', validators=[DataRequired()])
	email = TextField('Email address', validators=[DataRequired()])
	website = TextField('website')
	room_no = TextField('room number')
	rank = SelectField('rank', choices = [('ostadYar','ostadYar'), ('daneshYar','daneshYar'),
		 ('ostad tamam','ostad tamam'), ('ostad madov','ostad madov'),
		  ('bazneshaste','bazneshaste'), ('sayer','sayer')])
	pic = FileField('Image File')

class EditProfessorForm(Form):
	name = TextField('Professor name', [validators.Length(min=2, max=400)])
	email = TextField('email', [validators.Length(min=2, max=400)])
	website = TextField('website', [validators.Length(min=2, max=400)])
	delete_pic = SelectField('delete picture?', choices=[(False,'no'),(True,'yes')])
	pic = FileField()
	

class SearchForm(Form):
	search = TextField('search it')

class ProfRateForm(Form):
	clarity = IntegerField('Clarity', [validators.NumberRange(min=0, max=5)])
	easyness = IntegerField('Easyness', [validators.NumberRange(min=0, max=5)])
	helpfullness = IntegerField('Helpfullness', [validators.NumberRange(min=0, max=5)])
	study = TextField('Study', [validators.Length(min=4, max=25)])
	is_online = RadioField('online ? ')
	coolness = RadioField('Coolness')
	attendance = RadioField('Attendance')
	take_it_again = RadioField('take it again')
	course_axis = RadioField('Course Axis')
	excercises = RadioField('Excercises')
	Exam = RadioField('What about exam')
	scale = RadioField('anything about scaling')
	project = RadioField('what about course projects')
	hardness = RadioField('course hardness')
	gradign = RadioField('what about grading')
	
	
	
	
	
	
