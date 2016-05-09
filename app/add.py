from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import FacultyForm, ProfessorForm
from app.auth import requires_auth
# from PIL import Image
from werkzeug import secure_filename
add = Blueprint('add', __name__, template_folder='templates/add')

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
		form = FacultyForm(request.form)
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
		form = context.get('form')
		if form.validate:

			faculty = Faculty()
			faculty.name = form.name.data
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
			print form.pic.data
			fileName = secure_filename(form.pic.data.filename)
			# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			image = Image.open(fileName)
			prof.pic = image
			prof.save()
			faculty.professors.append(prof)
			faculty.save()
			return redirect(url_for('add.addprof'))
		return render_template('add/add-prof.html', **context)
add.add_url_rule('/add/prof', view_func=AddProf.as_view('addprof'))


