from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import ProfForFacForm, ProfForm, FacultyForm, UniversityForm
from mongoengine import Q
from flask import jsonify
from app.auth import requires_auth
from werkzeug import secure_filename
from app import app
from app.edit import save_image
import os
import tempfile
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

	def repeat_prof(self, form):
		if Professor.objects(email__contains = form.email.data).first() != None:
			return True
		tmp_prof =  Professor.objects(name__contains = replace_ye(form.name.data),
								faculty__id = form.faculty.data).first() 
		if tmp_prof != None:
			return True
		return False
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
			if self.repeat_prof(form):
				return redirect(url_for('user.user_add_prof', msg="repeatitive"))
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
			# msg = "you registered Professor " + prof.name + " successfully"
			form = self.get_pure_form()
			return redirect(url_for('user.user_add_prof', msg="successful"))

		return render_template('user/add-prof-user.html', profs = profs, form = form, msg="fail" )
	
user.add_url_rule('/user/add/professor', view_func = UserAddProfessor.as_view('user_add_prof'))

class UserAddFaculty(MethodView):
	def get_form(self):
		form = FacultyForm(request.form)
		form.uni.choices = [(str(u.id), u.name)for u in University.objects.all()]
		return form
	def get(self):
		form = self.get_form()		
		return render_template('user/add-fac-user.html',
								 form=form,
								 msg=request.args.get('msg'))
	def post(self):
		form = self.get_form()
		try:
			if form.validate():
				uni = University.objects(id = form.uni.data).first()
				if Faculty.objects(uni = uni, name__contains=form.name.data).first() != None:
					return redirect(url_for("user.user_add_faculty", msg="repeatitive"))

				fac = Faculty()
				fac.name = replace_ye(form.name.data)
				fac.uni = University.objects(id = form.uni.data).first()
				fac.published = False
				fac.save()
				return redirect(url_for("user.user_add_faculty", msg="successful"))
			return render_template("user/add-fac-user.html", form=form, msg="fail")
		except:
			return redirect(url_for("user.user_add_faculty", msg=fail))
user.add_url_rule("/user/add/faculty", view_func=UserAddFaculty.as_view("user_add_faculty"))

class UserAddUni(MethodView):
	def get(self):
		form = UniversityForm(request.form)
		msg = request.args.get("msg")
		return render_template('user/add-uni-user.html', form=form, msg=msg)
	def post(self):
		form = UniversityForm(request.form)
		if form.validate():
			if University.objects(name__contains = form.name.data).first() != None:
				return redirect(url_for("user.user_add_uni", msg="repeatitive"))
			University(name = replace_ye(form.name.data), published = False).save()
			return redirect(url_for("user.user_add_uni", msg="successful"))
		return render_template("user/add-uni-user.html", form=form, msg="fail")
user.add_url_rule("/user/add/uni", view_func=UserAddUni.as_view("user_add_uni"))

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



