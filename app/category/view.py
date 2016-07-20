from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import ProfForFacForm
from mongoengine import Q
from flask import jsonify


category = Blueprint('category', __name__, template_folder='templates/profile')

class CategoryView(MethodView):
	def get(self, fac_id):
		fac = Faculty.objects(id = fac_id).first()
		if fac:
			profs = Professor.objects(faculty = fac, published = True)
		else:
			prof = []
		form = ProfForFacForm()
		print 
		return render_template('category/faculty-view.html',
								 unis = University.objects(),
								 profs = profs,
								 form = form,
								 faculty = fac,
								 msg = request.args.get('msg')
								 )

class GetFaculty(MethodView):
	def post(self):
		print request.form.get("uni")
		print request.form.get("faculty")
		uni = University.objects(id = request.form.get("uni")).first()
		fac = Faculty.objects(uni = uni, id = request.form.get("faculty")).first()
		return redirect(url_for("category.faculty_view", fac_id = fac.id))

class FacultyView(MethodView):
	def get(self):
		return render_template('/profile/category-view.html', unis = University.objects.all())
	def post(self):
		print request.form.get("uni")
		print request.form.get("faculty")
		uni = University.objects(id = request.form.get("uni")).first()
		fac = Faculty.objects(uni = uni, id = request.form.get("faculty")).first()
		return redirect(url_for("category.faculty_view", fac_id = fac.id))

class FacultySearch(MethodView):
	def post(self):
		uni_id = request.json['uni']
		uni = University.objects(id = uni_id).first()
		faculties = Faculty.objects(uni = uni)

		# print [{"id":fac.id, "name":fac.name} for fac in faculties]
		return jsonify({"faculties": [{"id":str(fac.id), "text":fac.name} for fac in faculties]})

category.add_url_rule('/faculty/search', view_func = FacultySearch.as_view('facultySearch'))
category.add_url_rule('/faculty_view/<fac_id>', view_func=CategoryView.as_view('faculty_view'))
category.add_url_rule('/get_faculty', view_func=GetFaculty.as_view('get_faculty'))

category.add_url_rule('/category/', view_func = FacultyView.as_view('faculty'))
