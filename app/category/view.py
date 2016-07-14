from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask import jsonify


category = Blueprint('category', __name__, template_folder='templates/profile')

class CategoryView(MethodView):
	def get(self):
		unis = University.objects.all()
		return render_template('profile/fac.html', unis = unis, prof = [])
	def post(self):
		print request.form.get("uni")
		print request.form.get("faculty")
		uni = University.objects(id = request.form.get("uni")).first()
		fac = Faculty.objects(uni = uni, id = request.form.get("faculty")).first()
		profs = Professor.objects(faculty = fac)

		return render_template('profile/fac.html', unis = University.objects(), profs = profs)

class FacultySearch(MethodView):
	def post(self):
		uni_id = request.json['uni']
		uni = University.objects(id = uni_id).first()
		faculties = Faculty.objects(uni = uni)

		print [{"id":fac.id, "name":fac.name} for fac in faculties]
		return jsonify({"faculties": [{"id":str(fac.id), "text":fac.name} for fac in faculties]})

category.add_url_rule('/faculty/search', view_func = FacultySearch.as_view('facultySearch'))
category.add_url_rule('/category', view_func=CategoryView.as_view('category'))
