from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q

profile = Blueprint('profile', __name__, template_folder='templates/profile')

class ProfProfile(MethodView):
	def get_context(self,id):
		professor = Professor.objects.get_or_404(id=id)
		return professor
		
	def get(self,id):
		prof = self.get_context(id)
		return render_template('profile/professor.html', prof=prof)

class FacProfile(MethodView):
	def get_context(self,id):
		fac = Faculty.objects.get_or_404(id=id)
		return fac
	def get(self):
		fac = get_context(id)
		return render_template('profile/faculty.html', faculty=fac)

class UniProfile(MethodView):
	def get_context(self,id):
		uni = University.objects.get_or_404(id=id)
		return uni
	def get(self,id):
		uni = get_context(id)
		return render_template('profile/uni.html', uni=uni)
profile.add_url_rule('/prof/<id>', view_func=ProfProfile.as_view('prof profile'))
profile.add_url_rule('/fac/<id>', view_func=FacProfile.as_view('faculty profile'))
profile.add_url_rule('/uni/<id>', view_func=UniProfile.as_view('uni profile'))
