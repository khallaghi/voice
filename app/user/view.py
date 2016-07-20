from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import ProfForFacForm, ProfForm
from mongoengine import Q
from flask import jsonify
from app.auth import requires_auth
# from PIL import Image
from werkzeug import secure_filename
from app import app
from app.edit import save_image
import os
import tempfile
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
# import file
from app.utils import replace_ye


user = Blueprint('user', __name__, template_folder='templates/user')

class UserAddProfessor(MethodView):
	def get_context(self):
		form = ProfForm(request.form)      
		# form.faculty.choices = [(str(f.id), f.name +" -- " + f.uni.name) for f in Faculty.objects.all()]
		# form.faculty.choices = []
		form.uni.choices = [(str(u.id), u.name)for u in University.objects.all()]
		# form.faculty.choices = [(str(f.id), f.name)for f in Faculty.objects.all()]

		form.rank.choices = [('ostadYar','ostadYar'), ('daneshYar','daneshYar'),
		 ('ostad tamam','ostad tamam'), ('ostad madov','ostad madov'),
		  ('bazneshaste','bazneshaste'), ('sayer','sayer')]
		profs = Professor.objects.all()
		return {
			"profs": profs,
			"form" : form,
			"msg" : request.args.get("msg")
		}
	def get_pure_form(self):
		form = ProfForm()      
		form.uni.choices = [(str(u.id), u.name)for u in University.objects.all()]
		# form.faculty.choices = [(str(f.id), f.name)for f in Faculty.objects.all()]

		form.rank.choices = [('ostadYar','ostadYar'), ('daneshYar','daneshYar'),
		 ('ostad tamam','ostad tamam'), ('ostad madov','ostad madov'),
		  ('bazneshaste','bazneshaste'), ('sayer','sayer')]
		return form

	def get(self):
		context = self.get_context()
		return render_template('user/add-prof-user.html', **context)

	def post(self):
		msg = "this is some problem"
		context = self.get_context()
		form = context.get('form')
		profs = context.get('profs')
		print request.form.get('faculty')
		if form.validate():
			print "TRUE"
			# print form.faculty.data
			prof = Professor()
			prof.name = replace_ye(form.name.data)
			# prof.family = form.family.data
			prof.email = form.email.data
			prof.website = form.website.data
			faculty = Faculty.objects(id=request.form.get('faculty')).first()
			prof.faculty = faculty
			prof.save()
			save_image(request, prof)
			prof.published = False
			prof.save()
			faculty.professors.append(prof) 
			faculty.save()
			msg = "you registered Professor " + prof.name + " successfully"
			form = self.get_pure_form()
			return redirect(url_for('user.user_add_prof', msg="successful"))

		return render_template('user/add-prof-user.html', profs = profs, form = form, msg="fail" )
	
user.add_url_rule('/user/add/prof', view_func = UserAddProfessor.as_view('user_add_prof'))

class UserAddProfToFac(MethodView):
	def post(self, fac_id):
		form = ProfForFacForm(request.form)
		msg = "fail"
		if form.validate():
			prof = Professor()
			prof.name = form.name.data
			prof.email = form.email.data
			prof.website = form.website.data
			prof.room_no = form.room_no.data
			prof.rank = form.rank.data
			faculty = Faculty.objects(id = fac_id).first()
			prof.faculty = faculty
			save_image(request, prof)
			prof.published = False
			prof.save()
			faculty.professors.append(prof)
			faculty.save()
			msg = "successful"
		return redirect(url_for('category.faculty_view', 
										fac_id = fac_id,
										msg = msg))
user.add_url_rule('/user/add/proftofac/<fac_id>',
 view_func = UserAddProfToFac.as_view('user_add_prof_to_fac'))



