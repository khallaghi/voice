from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q

# from app.forms import FacultyForm, ProfessorForm
search = Blueprint('search', __name__, template_folder='templates/search')

class Search(MethodView):
	def search_result(self,keyword):
		profs = Professor.objects(Q(name__icontains=keyword) | Q(family__icontains=keyword))
		faculties = Faculty.objects(name__icontains=keyword)
		unis = University.objects(name__icontains=keyword)
		return {
			"profs" : profs,
			"faculties" : faculties,
			"unis" : unis
		}
	def get(self):
		# results = self.search_result(keyword)
		form = SearchForm(request.form)
		return render_template('search/search.html', form = form)
	def post(self):
		form = SearchForm(request.form)
		results = self.search_result(form.search.data)
		return render_template('search/search.html', form = form , **results)
search.add_url_rule('/search', view_func=Search.as_view('search'))
