from flask import Blueprint, request, redirect, render_template, url_for,\
send_from_directory
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import FacultyForm, ProfessorForm
from app.auth import requires_auth
from PIL import Image
from werkzeug import secure_filename
from app import app
import os
import tempfile
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
# import file
add = Blueprint('add', __name__, template_folder='templates/add')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class AddUni(MethodView):
	decorators = [requires_auth]
	form = model_form(University, exclude=['faculties'])
	def get_context(self):
		unis = University.objects.all()
		form = self.form(request.form)
		context = {
			"unis" : unis,
			"form" : form
		}
		return context
	def get(self):
		context = self.get_context()
		return render_template('add/add-uni.html', **context)

	def post(self):
		context = self.get_context()
		form = context.get('form')
		if form.validate():
			uni = University()
			form.populate_obj(uni)
			uni.save()
			return redirect(url_for('add.adduni'))
		return render_template('add/add-uni.html', **context)
add.add_url_rule('/add/uni', view_func=AddUni.as_view('adduni'))



class AddFaculty(MethodView):
	decorators = [requires_auth]
	def get_context(self):
		form = FacultyForm()
		form.uni.choices = [(uni.id, uni.name) for uni in University.objects.all() ]
		faculties = Faculty.objects.all()
		return {
			'faculties': faculties,
			'form' : form
			}

	def get(self):
		context = self.get_context()        
		# print context
		return render_template('add/add-faculty.html', **context)

	def post(self):
		context = self.get_context()
		# form = context.get('form')
		form = FacultyForm()
		if form.validate:

			faculty = Faculty()
			faculty.name = form.name.data
			print app.config['UPLOAD_FOLDER']
			print "***********************"
			print form.pic
			print "*************************"
			# print form.pic.file.filename
			image_data = request.files.get(form.pic.name)
			print "+++++++++++++++++++++++++++++"
			print image_data
			open(os.path.join(app.config['UPLOAD_FOLDER'], form.pic.name), 'w').write(image_data)

			print form.uni.data
			uni = University.objects(id=form.uni.data).first()
			faculty.uni = uni
			faculty.save()
			uni.faculties.append(faculty)
			uni.save()
			print faculty.uni
			print uni.name
			print len(uni.faculties)
			return redirect(url_for('add.addfac'))
		return render_template('add/add-faculty.html', **context)
add.add_url_rule('/add/fac', view_func=AddFaculty.as_view('addfac'))


class AddProf(MethodView):
	decorators = [requires_auth]
	def get_context(self):
		form = ProfessorForm(request.form)      
		form.faculty.choices = [(str(f.id), f.name) for f in Faculty.objects.all()]
		form.rank.choices = [('ostadYar','ostadYar'), ('daneshYar','daneshYar'),
		 ('ostad tamam','ostad tamam'), ('ostad madov','ostad madov'),
		  ('bazneshaste','bazneshaste'), ('sayer','sayer')]
		profs = Professor.objects.all()
		return {
			"profs": profs,
			"form" : form
		}
	def get(self):
		context = self.get_context()
		return render_template('add/add-prof.html', **context)
	def post(self):
		context = self.get_context()
		form = context.get('form')
		# form = ProfessorForm(request.form)
		print form.faculty.data
		if form.validate():
			print "TRUE"
			# print form.faculty.data
			prof = Professor()
			prof.name = form.name.data
			prof.family = form.family.data
			prof.email = form.email.data
			prof.website = form.website.data
			faculty = Faculty.objects(id=form.faculty.data).first()
			prof.faculty = faculty
			# print "------------------"
			# print form.pic.data
			# fileName = secure_filename(form.pic.data)
			# print "******"
			# print fileName
			filename = secure_filename(form.pic.data)
			form.pic.data.save(filename)

			# file = form.pic.data
			# print file
			# if file and allowed_file(file.filename):
			# 	filename = secure_filename(file.filename)
			# 	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# fileName.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			image = Image.open(filename)
			prof.pic = image
			prof.save()
			faculty.professors.append(prof)
			faculty.save()
			return redirect(url_for('add.addprof'))
		return render_template('add/add-prof.html', **context)
add.add_url_rule('/add/prof', view_func=AddProf.as_view('addprof'))


app.config['UPLOAD_FOLDER'] = 'uploaded_images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

class UploadFile(MethodView):
	def get(self):
		return render_template('add/index.html')
	def post(self):
		file = request.files['file']
		
		print "*********************"
		print file.filename
		print "*********************"
		print file
		
		if file and allowed_file(file.filename):
			print "in the if!"
			filename = secure_filename(file.filename)
			file.save(os.path.join("uploaded_images", filename))
			filename = os.path.join("uploaded_images", filename)
			print "filename is : "
			print filename
			image = Image.open(filename)
			print "image is : "
			print image
			# for prof in Professor.objects():
			prof = Professor.objects().first()
			if prof.pic:
				prof.pic.delete()
			prof.pic.put(filename)
			prof.save()

		return redirect(url_for('add.upload'))
add.add_url_rule('/upload', view_func=UploadFile.as_view('upload'))

class UploadedFile(MethodView):
	def get(self, filename):
		print "uploaded folder"
		print app.config['UPLOAD_FOLDER']
		return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)
add.add_url_rule('/uploaded_file/<filename>', view_func=UploadedFile.as_view('uploaded_file'))