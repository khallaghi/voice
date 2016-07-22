from flask import Blueprint, request, redirect, render_template, url_for, request
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask import jsonify


# from app.forms import FacultyForm, ProfessorForm
def ret_prof(profs):
	
	for prof in profs:
		ret_prof = {}	
		if prof.id:
			ret_prof['id'] = str(prof.id)
		if prof.name:
			ret_prof['name'] = prof.name
		if prof.faculty:
			ret_prof['faculty'] = prof.faculty.name
		if prof.faculty and prof.faculty.uni:
			ret_prof['uni'] = prof.faculty.uni.name
		ret_prof['img'] = prof.profile_pic
		yield ret_prof

def ret_faculty(faculties):
	for faculty in faculties:
		ret_faculty = {}

		ret_faculty['name'] = faculty.name
		ret_faculty['uni'] = faculty.uni.name
		yield ret_faculty

def ret_uni(unis):
	for uni in unis:
		ret_uni = {}
		ret_uni['name'] = uni.name
		yield ret_uni

def search_result(keyword):
	# profs = Professor.objects(Q(name__icontains=keyword))
	keyword = keyword.replace(u'\u064a', u'\u06cc')
	profs = Professor.objects.filter(
							(Q(name__icontains = keyword) | Q(studies__name__icontains = keyword)) &
							(Q(faculty__in = Faculty.objects(uni__in = University.objects(name__icontains = u'\u0634\u0631\u06cc\u0641')))) 

							)
	faculties = Faculty.objects(name__icontains=keyword)
	unis = University.objects(name__icontains=keyword)
	
	return {
		"profs" : [p for p in ret_prof(profs)],
		"faculties" : [f for f in ret_faculty(faculties)],
		"unis" : [u for u in ret_uni(unis)]
	}
search = Blueprint('search', __name__, template_folder='templates/search')
class Asghar(MethodView):
	
	def get(self, keyword):
		print "SSSSSSSSSSSSSSS"
		print keyword
		results = search_result(keyword)
		return jsonify(**results)

search.add_url_rule('/search/asghar/<keyword>', view_func=Asghar.as_view('Asghar'))

class Akbar(MethodView):
	
	def get(self):
		print "AKBAR"
		keyword = request.args.get('q')
		print keyword
		results = search_result(keyword)
		return jsonify(**results)

search.add_url_rule('/search/akbar/', view_func=Akbar.as_view('Akbar'))

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
search.add_url_rule('/', view_func=Search.as_view('search'))


class TestSearch(MethodView):
	def get(self):
		return render_template('search/new.html')
search.add_url_rule('/test', view_func=TestSearch.as_view("testSearch"))